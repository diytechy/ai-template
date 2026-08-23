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

from conftest import (
    ROOT,
    SCRIPTS,
    load_script,
    make_minimal_project,
    run_py,
)

from kitlib import ladder, stage as kitstage

DS = load_script("derive_stage")

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
def test_this_repo_s_committed_stage_is_current():
    """The meta-repo's own committed `docs/stage` records the live inputs. This is
    the same claim the commit-bar `--check` step makes; asserting it here too is
    what makes a stale commit visible to a plain `pytest` run as well."""
    recorded = kitstage.parse((ROOT / kitstage.STAGE_FILE).read_text(encoding="utf-8"))
    assert recorded is not None
    assert recorded["stage"] in ladder.LADDER_RUNGS
    assert recorded["fingerprint"] == kitstage.fingerprint(ROOT, memo=None)
    assert DS.read(ROOT)["source"] == "recorded"
