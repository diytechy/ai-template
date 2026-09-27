"""`derive_stage.py`: the EFFECTIVE stage derived from artifact states (TC-181).

WI-498 slice 1. Four of the deep-check's nine corner cases need real registry
rows and are driven here — the draft drop, the per-phase reading, the fresh
scaffold, and the claimed-branch lane. The other five are properties of the
carrier and live in `test_kitlib_stage.py`.

WHY EACH ONE IS AN ACCEPTANCE TEST AND NOT A NICETY: the deep-check drove every
one of them against the CURRENT code and found it real. The stage axis had no
draft counterfactual (so one ordinary Drafted row dropped a mature repo to what a
fresh scaffold reads — C-01 reproduced), no floor (so ord 0 was reachable, below
every runnable rung), no per-phase reading at all, and a fresh scaffold that
answered `None`. This module is the record that each of those now has a defined,
driven answer.
"""

import shutil
import subprocess

import pytest
from conftest import (
    ROOT,
    SCRIPTS,
    load_script,
    make_minimal_project,
    run_py,
    skip_without_env_gates,
)

from kitlib import ladder, stage as kitstage

DS = load_script("derive_stage")
CHECK = load_script("check")

SRS_H = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status,Phase\n"
)
LLRS_H = "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Phase\n"
TCS_H = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,"
    "Status,Phase\n"
)


def _sr(sid, status="Approved", sn="SN-001", phase=""):
    return '{},T,{},"r","why","ac",,M,Test,{},{}\n'.format(sid, sn, status, phase)


def _llr(lid, sr, status="Approved", phase=""):
    return '{},{},Adder,src/demo,add,"d",(see TC),{},{}\n'.format(
        lid, sr, status, phase
    )


def _tc(tid, verifies, status="Approved", phase=""):
    return '{},{},Unit,m,Smoke,"a=1","e",Yes,tests/test_demo.py::t,{},{}\n'.format(
        tid, verifies, status, phase
    )


def _write(scaffold, srs="", llrs="", tcs=""):
    req = scaffold / "docs" / "requirements"
    (req / "system-requirements.csv").write_text(SRS_H + srs, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(LLRS_H + llrs, encoding="utf-8")
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        TCS_H + tcs, encoding="utf-8"
    )


def _no_frame(scaffold):
    """Drop the two off-spine registries the ladder's INSERTED rungs read.

    Not a convenience: it is the shape of a project that adopts neither registry,
    which the rungs' declared applies-when explicitly serves ("a project that
    never declares a boundary is NOT held at DevStg-Boundary forever"). The frame
    rungs get their own test below rather than being silently absent.

    THE SECOND HALF OF THIS DOCSTRING USED TO RECORD A DEFECT AS A FIXTURE NEED,
    and it is worth keeping the correction visible. It read: "needed here because
    those two rungs are REPO-GLOBAL and sit BELOW every spine rung, so a
    scaffold's blank-but-present `external.toml` pins every phase at
    DevStg-Boundary and no spine-rung difference is observable at all." That was
    an accurate description of a defect that shipped to every adopter — the
    untouched, placeholder-only frame registries the scaffold installs held every
    repo at DevStg-Boundary forever — and deleting the files here is what kept
    the kit's own tests from ever seeing it (ROUND-SOL-RAW 2). `spine_rules`
    now reads a placeholder-only registry as NOT ADOPTED, so the deletion is no
    longer load-bearing; it stays because "adopts neither registry" is still a
    shape worth driving, and it is now driven ALONGSIDE the unmodified scaffold
    rather than instead of it (see
    `test_an_UNMODIFIED_bootstrap_reaches_Impl_on_a_settled_spine`)."""
    for name in ("external", "components"):
        for suffix in (".toml", ".csv"):
            path = scaffold / "docs" / "requirements" / (name + suffix)
            if path.exists():
                path.unlink()


def _settled_phase(name, sr, phase):
    """One phase whose single SR is Approved, decomposed and verified."""
    return (
        _sr(sr, phase=phase),
        _llr("LLR-" + name, sr, phase=phase),
        _tc("TC-" + name, sr, phase=phase),
    )


# --- corner case 1: a draft must not drop what the settled spine earned -------
def test_ONE_drafted_row_does_not_drop_the_effective_stage(scaffold):
    """C-01 ON THE NEW AXIS, refused. The deep-check drove it: a settled spine
    reads ord 7, and adding ONE ordinary Drafted requirement takes the LIVE stage
    to ord 2 — or to ord 0 if the draft happens to be a need — which under an
    at-or-above selection rule stops the test suite running at all. The depth of
    the drop is controlled by which TIER the draft lands in, a property of the
    drafted row that has nothing to do with the repo's maturity.

    The effective stage is derived over the SETTLED subset, so the draft is
    reported BESIDE it (`live-stage`, `drafted`) and never instead of it."""
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    srs, llrs, tcs = _settled_phase("001", "SR-001", "1")
    _write(scaffold, srs=srs, llrs=llrs, tcs=tcs)
    before = DS.derive(scaffold)

    # ...now one ordinary new requirement is drafted.
    _write(
        scaffold,
        srs=srs + _sr("SR-002", status="Drafted", phase="1"),
        llrs=llrs,
        tcs=tcs,
    )
    after = DS.derive(scaffold)

    assert after["stage"] == before["stage"], "a draft moved the effective stage"
    assert after["drafted"] == 1
    # the honest live reading DID drop, and says so beside the effective value
    assert after["live-stage"] == ladder.STAGE_REQS
    assert kitstage.order(after["live-stage"]) < kitstage.order(after["stage"])
    assert before["live-stage"] == before["stage"]


def test_a_draft_that_OPENS_A_NEW_PHASE_does_not_drop_it_either(scaffold):
    """The same defect wearing the shape it actually takes in this repo: a new
    delivery phase begins as drafted rows. The new phase has earned no rung, so it
    contributes no opinion to the fold — and it is still REPORTED, as the
    sentinel, because "this phase exists and has nothing settled" and "there is no
    such phase" are different facts."""
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    srs, llrs, tcs = _settled_phase("001", "SR-001", "1")
    _write(scaffold, srs=srs, llrs=llrs, tcs=tcs)
    before = DS.derive(scaffold)

    _write(
        scaffold,
        srs=srs + _sr("SR-002", status="Drafted", phase="2"),
        llrs=llrs,
        tcs=tcs,
    )
    after = DS.derive(scaffold)
    assert after["stage"] == before["stage"]
    assert after["per-phase"]["2"] == kitstage.BELOW
    assert after["per-phase-live"]["2"] == ladder.STAGE_REQS


# --- corner case 2: per-phase stages, and a global defined over them ----------
def test_per_phase_stages_exist_and_the_global_reading_is_defined_over_them(scaffold):
    """`spine_stage` took no phase argument and `_per_phase` folded BARS, so "the
    current phase's stage" did not exist — the deep-check's sharpest gap. It
    exists now, and the headline is the MIN over the phases that have earned
    something, so it is a fold of the breakdown rather than a second opinion
    beside it."""
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    srs1, llrs1, tcs1 = _settled_phase("001", "SR-001", "1")
    # phase 2: an approved requirement nobody has decomposed yet
    _write(
        scaffold,
        srs=srs1 + _sr("SR-002", phase="2"),
        llrs=llrs1,
        tcs=tcs1,
    )
    got = DS.derive(scaffold)

    assert set(got["per-phase"]) == {"1", "2"}
    assert got["per-phase"]["2"] == ladder.STAGE_LLREQS
    assert kitstage.order(got["per-phase"]["1"]) > kitstage.order(ladder.STAGE_LLREQS)
    # the global is the min over the phases that earned a rung
    assert got["stage"] == ladder.STAGE_LLREQS
    assert got["phase"] == 2


def test_the_need_coverage_rung_stays_REPO_GLOBAL_across_phases(scaffold):
    """The seam `cited_srs` exists for. The coverage question — does every
    approved need have a requirement answering it — is repo-wide: a need answered
    by phase 1's requirements is answered. Without the seam, running the
    derivation over one phase's rows reads every OTHER phase's needs as uncovered
    and reports DevStg-Needs for every phase but the first."""
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    srs1, llrs1, tcs1 = _settled_phase("001", "SR-001", "1")
    srs2, llrs2, tcs2 = _settled_phase("002", "SR-002", "2")
    _write(
        scaffold,
        srs=srs1 + srs2,
        llrs=llrs1 + llrs2,
        tcs=tcs1 + tcs2,
    )
    got = DS.derive(scaffold)
    assert ladder.STAGE_NEEDS not in got["per-phase"].values(), got["per-phase"]
    assert got["per-phase"]["1"] == got["per-phase"]["2"]


def test_the_FRAME_rungs_are_repo_global_and_cap_every_phase(scaffold):
    """The two INSERTED rungs (boundary, partition) read repo-wide registries and
    sit below every spine rung, so while the frame is in work EVERY phase reports
    the frame's rung however mature its own requirements are. That is honest —
    the boundary happens once, for the whole system — but it means the per-phase
    breakdown only discriminates once the frame settles, which is worth pinning
    rather than discovering later.

    It also drives the settled reading of those rows: a DRAFTED component is
    excluded from the settled subset exactly as a drafted requirement is.

    THE PREMISE WAS REPAIRED AT THE WI-498 CLOSE. This test used to lean on the
    scaffold's UNTOUCHED `external.toml` — "blank-but-present … a declared frame
    with no crossing typed is honestly incomplete" — which was the defect
    ROUND-SOL-RAW 2 measured, not a premise: the placeholder-only file the
    bootstrap ships is a frame nobody has adopted, and reading it as "declared
    and empty" pinned every adopting repo at DevStg-Boundary forever. The claim
    under test is unchanged and still worth pinning; it is now driven through a
    REAL declared crossing, which is what an adopted frame actually looks like."""
    make_minimal_project(scaffold)
    srs, llrs, tcs = _settled_phase("001", "SR-001", "1")
    _write(scaffold, srs=srs, llrs=llrs, tcs=tcs)
    # An ADOPTED frame: one real crossing, declared and not yet approved.
    ext = scaffold / "docs" / "requirements" / "external.toml"
    ext.write_text(
        ext.read_text(encoding="utf-8")
        + '\n[boundary.B-01]\nentity = "EXT-000"\ndirection = "in"\n'
        'carries = "A real crossing, declared and not yet approved."\n'
        'status = "Drafted"\n',
        encoding="utf-8",
    )
    framed = DS.derive(scaffold)
    assert framed["per-phase"]["1"] == ladder.STAGE_BOUNDARY
    assert framed["stage"] == kitstage.FLOOR and framed["floored"] is True

    _no_frame(scaffold)
    freed = DS.derive(scaffold)
    assert kitstage.order(freed["per-phase"]["1"]) > kitstage.order(
        ladder.STAGE_BOUNDARY
    )


# --- corner case 3: a fresh scaffold / an empty spine ------------------------
def test_a_fresh_scaffold_reads_a_DEFINED_non_raising_selection_value(scaffold):
    """Two opposite failure modes were driven on the old axis: before the first
    derivation there was no stage at all to read (`None`), and after it the stage
    was ord 0 — under at-or-above, a repo where NOTHING runs and the run goes
    green because of it, breaking the shipped promise that a freshly-scaffolded
    repo is green because its checks PASSED.

    The floor is the answer, and the honest ord-0 reading is reported beside
    it."""
    got = DS.derive(scaffold)
    assert got["stage"] == kitstage.FLOOR
    assert got["floored"] is True
    assert got["live-stage"] == ladder.STAGE_NEEDS
    assert got["settled-stage"] == kitstage.BELOW
    assert got["per-phase"] == {}
    # ... and the value is orderable, which is what selection will need
    assert kitstage.order(got["stage"]) == ladder.stage_ord(kitstage.FLOOR)


def test_an_UNMODIFIED_bootstrap_reaches_Impl_on_a_settled_spine(scaffold):
    """THE ACCEPTANCE TEST THE KIT DID NOT HAVE, and its absence is why a defect
    shipped to every adopter (ROUND-SOL-RAW 2, MAJOR).

    Every other rung test in this module calls `_no_frame` first, DELETING the
    two frame registries `bootstrap.py` installs. That is a legitimate shape —
    a project that adopts neither registry — but it was the ONLY shape driven,
    so the shape the kit actually SHIPS was never asserted on. On that shape a
    completely settled spine could not leave DevStg-Boundary: the placeholder
    `-000` rows filter out, the row list comes back empty, and an
    empty-but-present registry caps the rung. Measured on a real bootstrap
    before the fix: `settled-stage = DevStg-Boundary` with every SN/SR/LLR/TC
    row `Founded` — so `format`, `lint` and `tests+coverage` were unreachable
    from the derived value in every adopting repo, permanently.

    So: NO deletions, no edits to anything `bootstrap.py` wrote outside the
    spine. Fill the spine, approve it, and the ladder must climb.
    """
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    # The state under test: the scaffold's own frame registries, exactly as
    # bootstrap wrote them. Asserted rather than assumed — if a future bootstrap
    # stops shipping them, this test must stop claiming to cover this shape.
    external = req / "external.toml"
    components = req / "components.toml"
    assert external.exists() and components.exists(), (
        "bootstrap no longer ships the frame registries — this test's premise "
        "is gone and the test must be re-aimed, not deleted"
    )
    shipped = (
        external.read_text(encoding="utf-8"),
        components.read_text(encoding="utf-8"),
    )
    # A fully settled spine: every tier Founded (settled AND demonstrated).
    _write(
        scaffold,
        srs=_sr("SR-001", status="Founded"),
        llrs=_llr("LLR-001", "SR-001", status="Founded"),
        tcs=_tc("TC-001", "SR-001;LLR-001", status="Founded"),
    )
    got = DS.derive(scaffold)
    assert got["settled-stage"] == ladder.STAGE_IMPL, (
        "a settled spine on the scaffold the kit SHIPS must reach Impl; it read "
        + str(got["settled-stage"])
    )
    assert got["stage"] == ladder.STAGE_IMPL
    # ...and it got there without the test touching the frame files.
    assert (
        external.read_text(encoding="utf-8"),
        components.read_text(encoding="utf-8"),
    ) == shipped, "the frame registries were modified — the premise is void"
    # The rungs are NOT disarmed: writing one real row into the shipped file is
    # an adoption act, and a Drafted crossing correctly caps the ladder again.
    external.write_text(
        shipped[0] + '\n[boundary.B-01]\nentity = "EXT-000"\ndirection = "in"\n'
        'carries = "A real crossing."\nstatus = "Drafted"\n',
        encoding="utf-8",
    )
    assert DS.derive(scaffold)["settled-stage"] == ladder.STAGE_BOUNDARY, (
        "a real Drafted crossing must still hold the boundary rung — the fix "
        "must read placeholders as unadopted, not switch the rung off"
    )


def test_an_ALL_DRAFT_spine_also_lands_on_the_floor(scaffold):
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    _write(scaffold, srs=_sr("SR-001", status="Drafted", phase="1"))
    got = DS.derive(scaffold)
    assert got["stage"] == kitstage.FLOOR
    assert got["floored"] is True
    assert got["per-phase"] == {"1": kitstage.BELOW}


# --- corner case 8: the claimed-branch lane ----------------------------------
def test_on_a_CLAIMED_BRANCH_the_reader_derives_from_the_branch_s_own_registries(
    scaffold,
):
    """W-1, THE LARGEST STALE WINDOW THE SCHEDULE MAP FOUND, closed by
    construction. `derived-stage` is a member of `_TRUNK_FRESHNESS_STEPS`, so it
    reports SKIP on any claimed work branch — and a skipped step never affects the
    exit code, which makes a GREEN run over a stale cache reachable there and
    nowhere else.

    The common reader does not depend on that step: it verifies per call, so on a
    claimed branch it derives from the branch's OWN registries. That is the trust
    model the owner confirmed (§6.4) — spine work happens in series, so the
    branch's derived result IS the trunk's next value.

    It also must not WRITE there: a work branch never commits a generated
    artifact, and a self-healing reader would make it do exactly that."""
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    srs, llrs, tcs = _settled_phase("001", "SR-001", "1")
    _write(scaffold, srs=srs, llrs=llrs, tcs=tcs)
    assert (
        run_py(
            [SCRIPTS / "derive_stage.py", "--root", scaffold], cwd=scaffold
        ).returncode
        == 0
    )
    recorded = (scaffold / kitstage.STAGE_FILE).read_text(encoding="utf-8")
    trunk_value = kitstage.parse(recorded)["stage"]

    # the lane marker check.py reads to stand its freshness step down
    (scaffold / "docs" / "work" / "active" / "wi999-lane").mkdir(
        parents=True, exist_ok=True
    )
    # ...and the branch edits the spine, leaving the committed copy stale
    _write(scaffold, srs=srs + _sr("SR-002", phase="2"), llrs=llrs, tcs=tcs)

    got = DS.read(scaffold)
    assert got["source"] == "derived"
    assert got["stage"] == ladder.STAGE_LLREQS != trunk_value
    assert (scaffold / kitstage.STAGE_FILE).read_text(encoding="utf-8") == recorded


# --- the producer's own contract ---------------------------------------------
def test_write_then_check_roundtrips(scaffold):
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    write = run_py([SCRIPTS / "derive_stage.py", "--root", scaffold], cwd=scaffold)
    assert write.returncode == 0, write.stdout + write.stderr
    check = run_py(
        [SCRIPTS / "derive_stage.py", "--root", scaffold, "--check"], cwd=scaffold
    )
    assert check.returncode == 0, check.stdout + check.stderr
    assert "up to date" in check.stdout


def test_check_detects_state_drift(scaffold):
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    run_py([SCRIPTS / "derive_stage.py", "--root", scaffold], cwd=scaffold)
    _write(scaffold, srs=_sr("SR-001") + _sr("SR-002", phase="9"))
    drift = run_py(
        [SCRIPTS / "derive_stage.py", "--root", scaffold, "--check"], cwd=scaffold
    )
    assert drift.returncode == 1
    assert "STALE" in drift.stderr


def test_check_on_an_ABSENT_file_asks_for_the_first_generation(scaffold):
    """Distinct from the placeholder case below: a scaffold SHIPS the file, so an
    absent one means it was deleted or an adopter has not resynced. That is a
    hard fail with an actionable message, not a note."""
    (scaffold / kitstage.STAGE_FILE).unlink()
    proc = run_py(
        [SCRIPTS / "derive_stage.py", "--root", scaffold, "--check"], cwd=scaffold
    )
    assert proc.returncode == 1
    assert "absent" in proc.stderr


def test_the_written_file_is_LF_and_parses_back(scaffold):
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    run_py([SCRIPTS / "derive_stage.py", "--root", scaffold], cwd=scaffold)
    raw = (scaffold / kitstage.STAGE_FILE).read_bytes()
    assert b"\r\n" not in raw
    assert kitstage.parse(raw.decode("utf-8")) is not None


def test_the_check_py_STEP_goes_red_on_a_stale_cache(scaffold):
    """NON-VACUITY, at the level the claim is actually made. The script's own
    `--check` is driven above, but what the commit bar runs is `check.py`'s
    `derived-stage` STEP — a step can be wired and still be unable to fail (the
    exact silent green SN-008 forbids). So: plant the defect, run the step, and
    require a non-zero exit."""
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    run_py([SCRIPTS / "derive_stage.py", "--root", scaffold], cwd=scaffold)
    green = run_py(
        [scaffold / "scripts" / "check.py", "--run-steps", "derived-stage"],
        cwd=scaffold,
    )
    assert green.returncode == 0, green.stdout + green.stderr

    _write(scaffold, srs=_sr("SR-001", phase="1") + _sr("SR-002", phase="7"))
    red = run_py(
        [scaffold / "scripts" / "check.py", "--run-steps", "derived-stage"],
        cwd=scaffold,
    )
    assert red.returncode != 0, red.stdout + red.stderr
    assert "derived-stage" in red.stdout + red.stderr


def test_a_freshly_scaffolded_repo_is_GREEN_on_the_placeholder(scaffold):
    """The shipped promise (`ci/check.yml`: "a freshly-scaffolded DevStg-Reqs repo
    is green") must survive the new step. The scaffold ships a comment-only
    placeholder rather than invented values, and `--check` passes it with a note
    — the same smooth-transition path `docs/gate` gives a legacy hand-set marker.
    Green because there is genuinely nothing to be stale against, not because the
    check was sanctioned."""
    assert (scaffold / kitstage.STAGE_FILE).exists()
    assert (
        kitstage.parse((scaffold / kitstage.STAGE_FILE).read_text(encoding="utf-8"))
        is None
    )
    proc = run_py(
        [scaffold / "scripts" / "check.py", "--run-steps", "derived-stage"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- WI-402: --next-phase, the derived next phase as an output mode -----------
# MOVED HERE FROM tests/test_spine_rules.py AT WI-498 SLICE 5, with the CLI it
# drives: `--next-phase` was rehomed from the retired `derive_gate.py` CLI onto
# this module, which already derives `phase` from the same rows by the same rule.
# The WI-402 ruling the two tests record is still live, and `--next-phase` is
# still taught in PROCESS.md, PROCESS_OPTIONS.md and RESYNC_PACK.md — so the pin
# moves rather than retires. The "does not write" assertion moves with it, from
# `docs/gate` to `docs/stage`.
def _phased_srs(scaffold):
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        SRS_H
        + _sr("SR-001", phase="1")
        + _sr("SR-002", phase="3")
        # A Drafted row in a higher phase: its phase is not yet scope.
        + _sr("SR-003", status="Drafted", phase="4"),
        encoding="utf-8",
    )


def test_next_phase_prints_max_plus_one(scaffold):
    # --next-phase = max(phase over non-draft spine rows) + 1, printed bare so
    # the intake mint helper (WI-388) can shell out and int() the answer when a
    # confirmed scope change opens a new phase. A Drafted row's phase is not yet
    # scope, so it never bumps the answer — same derivation as the record's
    # phase=N, exposed as an output mode.
    make_minimal_project(scaffold)
    _phased_srs(scaffold)
    stage_file = scaffold / kitstage.STAGE_FILE
    before = stage_file.read_text(encoding="utf-8")
    proc = run_py(
        [SCRIPTS / "derive_stage.py", "--root", scaffold, "--next-phase"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == "4"  # max approved = 3; the Drafted 4 is excluded
    # An output mode over the existing derivation: docs/stage is not rewritten.
    assert stage_file.read_text(encoding="utf-8") == before


def test_next_phase_on_an_unphased_spine(scaffold):
    # An unphased spine is the implicit foundation (phase 1) — what blank bought
    # before the phase model — so the first opened phase is 2, never 1, which
    # would collapse the new scope into the foundation the blank rows occupy.
    make_minimal_project(scaffold)
    proc = run_py(
        [SCRIPTS / "derive_stage.py", "--root", scaffold, "--next-phase"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == "2"


# --- the dogfood --------------------------------------------------------------
def _assert_committed_stage_current(root):
    """`root`'s committed `docs/stage` records the live inputs, or SKIP on a
    claimed work branch.

    The skip is the commit-bar twin's: check.py stands the `derived-stage` step
    down on a claimed work branch because generated freshness is the trunk
    lane's (concurrency-restructure §5.2). It asks `check._work_branch`, the
    same detector, so there is one notion of "work branch", fail-closed: off
    git, detached, or unclaimed, the claim is asserted in full."""
    branch = CHECK._work_branch(root)
    if branch:
        pytest.skip(
            "work branch '{}': the committed stage's freshness is the trunk "
            "lane's, as for check.py's derived-stage step".format(branch)
        )
    recorded = kitstage.parse((root / kitstage.STAGE_FILE).read_text(encoding="utf-8"))
    assert recorded is not None
    assert recorded["stage"] in ladder.LADDER_RUNGS
    assert recorded["fingerprint"] == kitstage.fingerprint(root, memo=None)
    assert DS.read(root)["source"] == "recorded"


def test_this_repo_s_committed_stage_is_current():
    """The meta-repo's own committed `docs/stage` records the live inputs. This is
    the same claim the commit-bar `--check` step makes; asserting it here too is
    what makes a stale commit visible to a plain `pytest` run as well."""
    _assert_committed_stage_current(ROOT)


def test_the_stage_currency_claim_stands_down_on_a_claimed_branch_only(scaffold):
    """The claim above is exempt where its commit-bar twin is, and nowhere else.
    Amending a settled row moves the stage's input digest, so a claimed work
    branch doing the routine amendment meets a stale `docs/stage` it may not
    regenerate; the trunk, with the same stale file, must still go red."""
    skip_without_env_gates("git")
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    srs, llrs, tcs = _settled_phase("001", "SR-001", "1")
    _write(scaffold, srs=srs, llrs=llrs, tcs=tcs)
    write = run_py([SCRIPTS / "derive_stage.py", "--root", scaffold], cwd=scaffold)
    assert write.returncode == 0, write.stdout + write.stderr

    def on_branch(branch):
        git = shutil.which("git")
        for args in (["init", "-q"], ["symbolic-ref", "HEAD", "refs/heads/" + branch]):
            subprocess.run([git, "-C", str(scaffold), *args], check=True)
        CHECK._WORK_BRANCH_CACHE.clear()

    on_branch("main")
    _assert_committed_stage_current(scaffold)  # fresh on the trunk: the baseline

    # A settled row amended, its status left Approved: the recorded copy is stale.
    _write(scaffold, srs=srs.replace('"r"', '"r, amended"'), llrs=llrs, tcs=tcs)
    with pytest.raises(AssertionError):
        _assert_committed_stage_current(scaffold)

    # The same tree on a claimed work branch: the claim stands down.
    on_branch("wi-999-lane")
    claim = scaffold / "docs" / "work" / "active" / "wi-999-lane"
    claim.mkdir(parents=True)
    (claim / "WI-999-demo.md").write_text('+++\nid = "WI-999"\n+++\n', encoding="utf-8")
    with pytest.raises(pytest.skip.Exception):
        _assert_committed_stage_current(scaffold)


# --- TC-226: an assumption-only case joins its requirements' phases (SR-197) ---
# An assumption has no phase of its own; a test case evidencing one belongs to
# every phase of the requirements whose arguments rely on it (LLR-230).


def _row(id_col, rid, **cells):
    return dict({id_col: rid}, **cells)


PHASED = [
    _row("SR-ID", "SR-001", Phase="5", **{"DA-Refs": "DA-001", "SN-Refs": "SN-001"}),
    _row("SR-ID", "SR-002", Phase="6", **{"DA-Refs": "DA-001", "SN-Refs": "SN-001"}),
]


def _placed(groups, tid):
    return sorted(
        label
        for label, (_s, _l, tcs) in groups.items()
        if tid in [t["TC-ID"] for t in tcs]
    )


def test_an_assumption_only_case_joins_each_phase_citing_its_assumption():
    tcs = [
        _row("TC-ID", "TC-001", **{"Assumption-Refs": "DA-001"}),
        _row("TC-ID", "TC-002", **{"Assumption-Refs": "DA-009"}),
    ]
    da_srs = DS.assumption_rules.da_citing_srs(PHASED)
    groups = DS._phase_groups(PHASED, [], tcs, da_srs)
    assert _placed(groups, "TC-001") == ["5", "6"]
    # A case whose assumption no requirement cites is placed in no phase.
    assert _placed(groups, "TC-002") == []
    # Without the map the call reads exactly as it did before the parameter.
    assert _placed(DS._phase_groups(PHASED, [], tcs), "TC-001") == []


def test_the_stage_map_places_the_case_itself():
    """`_stage_map` derives the map from the requirements it is handed, so a
    Drafted assumption-only case holds BOTH phases' live reading at Tests."""
    srs = [dict(r, Status="Approved", Verification="Test") for r in PHASED]
    llrs = [
        _row("LLR-ID", "LLR-001", **{"SR-Refs": "SR-001", "Status": "Approved"}),
        _row("LLR-ID", "LLR-002", **{"SR-Refs": "SR-002", "Status": "Approved"}),
    ]
    tcs = [
        _row("TC-ID", "TC-001", Verifies="SR-001;LLR-001", Status="Approved"),
        _row("TC-ID", "TC-002", Verifies="SR-002;LLR-002", Status="Approved"),
        _row("TC-ID", "TC-003", Status="Drafted", **{"Assumption-Refs": "DA-001"}),
    ]
    spine = dict(
        srs=srs,
        llrs=llrs,
        tcs=tcs,
        sn_ids={"SN-001"},
        sn_draft=set(),
        bifs=[],
        cmps=[],
        have_bifs=False,
        have_cmps=False,
    )
    _live, per_phase = DS._stage_map(spine, settled=False)
    assert per_phase == {"5": ladder.STAGE_TESTS, "6": ladder.STAGE_TESTS}
    spine["tcs"] = tcs[:2]
    _live, per_phase = DS._stage_map(spine, settled=False)
    assert per_phase == {"5": ladder.STAGE_IMPL, "6": ladder.STAGE_IMPL}


def _toml_spine(root, assumption):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (root / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (req / "stakeholder-needs.md").write_text(
        "# Stakeholder needs\n\n## SN-001 — A demo need [Approved]\n\nBody.\n",
        encoding="utf-8",
        newline="\n",
    )
    srs = "".join(
        '[requirement.{}]\ntitle = "T"\nsn_refs = ["SN-001"]\nrequirement = "r"\n'
        'rationale = "why"\nacceptance_criteria = "ac"\npriority = "M"\n'
        'verification = "Test"\nstatus = "Approved"\nphase = {}\n'
        'da_refs = ["{}"]\n\n'.format(sid, phase, did)
        for sid, phase, did in (("SR-001", 5, "DA-001"), ("SR-002", 6, "DA-002"))
    )
    (req / "system-requirements.toml").write_text(srs, encoding="utf-8", newline="\n")
    (req / "low-level-requirements.toml").write_text("", encoding="utf-8")
    (root / "docs" / "test" / "test-cases.toml").write_text(
        '[test.TC-003]\nlevel = "Unit"\nmethod = "m"\ntier = "Full"\n'
        'expected = "e"\nautomated = "No"\nstatus = "Approved"\n'
        'assumption_refs = ["{}"]\n'.format(assumption),
        encoding="utf-8",
        newline="\n",
    )


def test_a_moved_assumption_reference_is_attributed_to_the_case_s_phases(tmp_path):
    import subprocess

    from conftest import pin_autocrlf

    def git(*args):
        subprocess.run(
            ["git", "-C", str(tmp_path), *args], check=True, capture_output=True
        )

    git("init", "-q")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "T")
    git("config", "commit.gpgsign", "false")
    pin_autocrlf(tmp_path)
    _toml_spine(tmp_path, "DA-001")
    git("add", "-A")
    git("commit", "-q", "-m", "state")
    _toml_spine(tmp_path, "DA-002")

    before = DS._spine_at(tmp_path, "HEAD")
    live = DS.spine_rules.load_spine(tmp_path / "docs")
    changed = DS._changed_rows(live, DS._by_id(before))
    assert [(rid, key, moved) for rid, key, _row, moved in changed] == [
        ("TC-003", "tcs", "Assumption-Refs DA-001 -> DA-002")
    ]

    def phases(spine):
        da_srs = DS.assumption_rules.da_citing_srs(spine["srs"])
        return _placed(
            DS._phase_groups(spine["srs"], spine["llrs"], spine["tcs"], da_srs),
            "TC-003",
        )

    assert phases(before) == ["5"]
    assert phases(live) == ["6"]


# --- TC-236: the assumption, surrogate and stakeholder tiers join the stage at
# their first approval, each tier read on its own (SR-204, LLR-241) ----------
# A tier holding only Drafted rows reads, to its rung, as a frame declared and
# not approved; reading it before its first approval would lower the derived
# stage of every tree in between. So a tier is read only once one of its rows
# is Approved, and then a Drafted row of it holds its rung in the live reading.


def _settled_spine(**tiers):
    """An in-memory spine every spine row of which is settled, no frame, and the
    three tiers under test as given: the live and settled readings are both
    DevStg-Impl until a tier holds a rung."""
    spine = dict(
        srs=[
            _row(
                "SR-ID",
                "SR-001",
                Status="Approved",
                Verification="Test",
                **{"SN-Refs": "SN-001"},
            )
        ],
        llrs=[_row("LLR-ID", "LLR-001", Status="Approved", **{"SR-Refs": "SR-001"})],
        tcs=[_row("TC-ID", "TC-001", Status="Approved", Verifies="SR-001;LLR-001")],
        sn_ids={"SN-001"},
        sn_draft=set(),
        bifs=[],
        cmps=[],
        have_bifs=False,
        have_cmps=False,
        das=[],
        surs=[],
        stks=[],
    )
    spine.update(tiers)
    return spine


def _readings(spine):
    """`(live, settled)` over the in-memory spine."""
    live, _ = DS._stage_map(spine, settled=False)
    settled, _ = DS._stage_map(spine, settled=True)
    return live, settled


def _da(did, status):
    return _row("DA-ID", did, Status=status)


def _sur(sid, status):
    return _row("SUR-ID", sid, Status=status)


def _stk(sid, status):
    return _row("STK-ID", sid, Status=status)


IMPL = (ladder.STAGE_IMPL, ladder.STAGE_IMPL)


def test_a_tier_holding_only_drafted_rows_moves_neither_reading():
    assert _readings(_settled_spine()) == IMPL
    for tiers in (
        {"das": [_da("DA-001", "Drafted"), _da("DA-002", "Drafted")]},
        {"surs": [_sur("SUR-001", "Drafted")]},
        {"stks": [_stk("STK-01", "Drafted"), _stk("STK-02", "Drafted")]},
    ):
        assert _readings(_settled_spine(**tiers)) == IMPL, tiers


def test_after_the_first_approval_a_draft_holds_its_rung_in_the_live_reading_only():
    held = {
        "das": ([_da("DA-001", "Approved"), _da("DA-002", "Drafted")], "BOUNDARY"),
        "surs": ([_sur("SUR-001", "Approved"), _sur("SUR-002", "Drafted")], "BOUNDARY"),
        "stks": ([_stk("STK-01", "Approved"), _stk("STK-02", "Drafted")], "NEEDS"),
    }
    for key, (rows, rung) in held.items():
        live, settled = _readings(_settled_spine(**{key: rows}))
        assert live == getattr(ladder, "STAGE_" + rung), key
        assert settled == ladder.STAGE_IMPL, key
    # With every row of each tier approved, nothing holds.
    assert (
        _readings(
            _settled_spine(
                das=[_da("DA-001", "Approved")],
                surs=[_sur("SUR-001", "Approved")],
                stks=[_stk("STK-01", "Approved")],
            )
        )
        == IMPL
    )


def test_the_two_tiers_sharing_the_assumptions_file_stay_apart():
    """An approved assumption does not activate the surrogate tier, and an
    approved surrogate does not activate the assumption tier."""
    assert (
        _readings(
            _settled_spine(
                das=[_da("DA-001", "Approved")], surs=[_sur("SUR-001", "Drafted")]
            )
        )
        == IMPL
    )
    assert (
        _readings(
            _settled_spine(
                das=[_da("DA-001", "Drafted")], surs=[_sur("SUR-001", "Approved")]
            )
        )
        == IMPL
    )


def test_no_setting_turns_a_tier_on():
    """`tier_active` reads the rows and nothing else: the one input is whether
    any row of the tier reads Approved (LLR-241; Founded does not count)."""
    rules = DS.spine_rules
    assert not rules.tier_active([])
    assert not rules.tier_active([_da("DA-001", "Drafted")])
    assert rules.tier_active([_da("DA-001", "Drafted"), _da("DA-002", "Approved")])
    assert rules.tier_active([_da("DA-001", "approved")])
    # "Reads Approved" is the switch (LLR-241): a tier whose only non-draft row
    # reads Founded holds no Approved row, so it is not read.
    assert not rules.tier_active([_sur("SUR-001", "Founded")])


def _needs_file(root, need_status, stakeholder_status):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (root / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (req / "stakeholder-needs.toml").write_text(
        '[need.SN-001]\nstatus = "{}"\nneed = "A need."\nwhy = "Why."\n'
        'priority = "M"\nacceptance = "Seen."\nstakeholder_refs = ["STK-01"]\n\n'
        '[stakeholder.STK-01]\nname = "Operator"\ndescription = "Runs it."\n'
        'status = "{}"\n\n'
        '[stakeholder.STK-02]\nname = "Reviewer"\ndescription = "Reads it."\n'
        'status = "Approved"\n'.format(need_status, stakeholder_status),
        encoding="utf-8",
        newline="\n",
    )
    (req / "system-requirements.toml").write_text(
        '[requirement.SR-001]\ntitle = "T"\nsn_refs = ["SN-001"]\n'
        'requirement = "r"\nrationale = "why"\nacceptance_criteria = "ac"\n'
        'priority = "M"\nverification = "Test"\nstatus = "Approved"\n',
        encoding="utf-8",
        newline="\n",
    )
    (req / "low-level-requirements.toml").write_text(
        '[design.LLR-001]\nsr_refs = ["SR-001"]\ntitle = "t"\nmodule = "m.py"\n'
        'code_symbol = "f"\ndetail = "d"\nstatus = "Approved"\n',
        encoding="utf-8",
        newline="\n",
    )
    (root / "docs" / "test" / "test-cases.toml").write_text(
        '[test.TC-001]\nverifies = ["SR-001", "LLR-001"]\nlevel = "Unit"\n'
        'method = "m"\ntier = "Smoke"\nexpected = "e"\nautomated = "Yes"\n'
        'evidence = "tests/t.py::t"\nstatus = "Approved"\n',
        encoding="utf-8",
        newline="\n",
    )


def test_a_stakeholder_s_status_never_answers_for_a_need(tmp_path):
    """The two tiers share the needs file and are loaded by their own id
    columns: a Drafted stakeholder beside an approved need is not a drafted
    need, and an approved stakeholder does not settle a Drafted need."""
    drafted_stk = tmp_path / "drafted-stakeholder"
    _needs_file(drafted_stk, "Approved", "Drafted")
    spine = DS.spine_rules.load_spine(drafted_stk / "docs")
    assert spine["sn_draft"] == set()
    assert [r["STK-ID"] for r in spine["stks"]] == ["STK-01", "STK-02"]
    record = DS.derive(drafted_stk)
    # The stakeholder tier is active (STK-02) and STK-01 is Drafted: the live
    # reading holds at Needs through the STAKEHOLDER rung, the settled one not.
    assert record["live-stage"] == ladder.STAGE_NEEDS
    assert record["settled-stage"] == ladder.STAGE_IMPL

    drafted_need = tmp_path / "drafted-need"
    _needs_file(drafted_need, "Drafted", "Approved")
    spine = DS.spine_rules.load_spine(drafted_need / "docs")
    assert spine["sn_draft"] == {"SN-001"}
    assert DS.derive(drafted_need)["live-stage"] == ladder.STAGE_NEEDS


def test_derive_counts_the_three_tiers_drafts(tmp_path):
    _needs_file(tmp_path, "Approved", "Drafted")
    (tmp_path / "docs" / "requirements" / "assumptions.toml").write_text(
        '[assumption.DA-001]\neffect_at = ["B-01"]\nassumption = "a"\n'
        'holds_when = "h"\nobstacle = "o"\nstatus = "Drafted"\nstanding = "active"\n\n'
        '[surrogate.SUR-001]\nname = "s"\nemulates = ["EXT-001"]\n'
        'description = "d"\nstatus = "Drafted"\n',
        encoding="utf-8",
        newline="\n",
    )
    spine = DS.spine_rules.load_spine(tmp_path / "docs")
    assert [r["DA-ID"] for r in spine["das"]] == ["DA-001"]
    assert [r["SUR-ID"] for r in spine["surs"]] == ["SUR-001"]
    # One Drafted stakeholder, one assumption, one surrogate.
    assert DS.derive(tmp_path)["drafted"] == 3


def test_the_scaffold_s_template_rows_hold_nothing(scaffold):
    """A freshly scaffolded tree carries the assumptions template's `-000`
    example rows and the needs template's example stakeholder; neither is a
    real row, so the three tiers read empty and hold nothing."""
    spine = DS.spine_rules.load_spine(scaffold / "docs")
    assert spine["das"] == [] and spine["surs"] == [] and spine["stks"] == []


def test_the_derivation_reads_the_assumptions_registry_as_a_declared_input(
    tmp_path,
):
    """The derivation reads no policy file, and every file it reads is a
    declared input of the fingerprint, the assumptions registry among them."""
    import io
    from pathlib import Path
    from unittest import mock

    _needs_file(tmp_path, "Approved", "Approved")
    req = tmp_path / "docs" / "requirements"
    (req / "assumptions.toml").write_text(
        '[surrogate.SUR-001]\nname = "s"\nemulates = ["EXT-001"]\n'
        'description = "d"\nstatus = "Approved"\n',
        encoding="utf-8",
        newline="\n",
    )
    (tmp_path / "docs" / "process.toml").write_text(
        '[attestation]\nhuman_approval_through = "DevStg-Reqs"\n', encoding="utf-8"
    )
    opened = []
    real_open = io.open

    def _audit(file, *args, **kwargs):
        try:
            opened.append(Path(file).resolve())
        except TypeError:
            pass
        return real_open(file, *args, **kwargs)

    with mock.patch("io.open", _audit), mock.patch("builtins.open", _audit):
        DS.spine_rules.load_spine(tmp_path / "docs")
    declared = {
        p.resolve() for _d, p in kitstage.input_paths(tmp_path) if p is not None
    }
    assert (req / "assumptions.toml").resolve() in declared
    assert (req / "assumptions.toml").resolve() in opened
    assert (tmp_path / "docs" / "process.toml").resolve() not in opened
    docs = (tmp_path / "docs").resolve()
    assert {p for p in opened if p.is_relative_to(docs)} <= declared


def test_the_new_maturity_tables_equal_the_check_s_enum_vocabulary():
    """Compared case-normalized, as the approval-level test pins the existing
    tables: the tables are keyed lowercase because `_maturity` lowercases."""
    rules = DS.spine_rules
    trace = load_script("trace")
    vocabulary = {v.lower() for v in trace.ENUM_FIELDS["STK"]["Status"]}
    assert set(rules.STK_MATURITY) == vocabulary
    # The assumption tier's status vocabulary is the spine's closed one, which
    # `assumption_rules` judges its two tiers against.
    spine_vocabulary = {v.lower() for v in DS.assumption_rules.STATUS_VALUES}
    assert set(rules.DA_MATURITY) == spine_vocabulary
    assert set(rules.SUR_MATURITY) == spine_vocabulary
