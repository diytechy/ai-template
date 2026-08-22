"""Check selection is AT OR ABOVE the derived stage (OI-51, ruled 2026-08-21).

THE OWNER'S RULE: a step runs because the repo IS AT OR ABOVE the rung the step
becomes relevant at — *"when is it relevant for me to run these checks"* — never
because some earlier bar was cleared.

THIS FILE SUCCEEDS `test_product_floor.py`, and the succession is the point.
WI-473 built a monotonic PRODUCT-REGRESSION FLOOR because the derived bar was a
MIN over every in-scope row, so one ordinary draft dropped a mature project to
what a fresh scaffold reads and product checks stopped running (repo review
2026-08-19 C-01). The floor compensated for that on one layer. WI-498 removes the
cause instead: `docs/stage`'s effective stage is derived over the SETTLED spine,
so drafting cannot lower selection for ANY step, and the floor — plus the
advisory tier that covered the same blind spot warn-only — retired with it.

So the C-01 regression scenario the review asked for is driven here at the
SELECTION level, which is where it now lives. The floor's own honesty tripwire
(`test_the_floor_is_dormant_for_the_BUILT_IN_product_steps_and_says_so`) had a
successor obligation written into it — *"which bar those three belong at is a
policy question with an owner ruling already sitting on it (OI-51); this test
exists so nobody reads the floor as having fixed it"* — and
`test_the_three_built_in_product_steps_are_REACHABLE_from_a_derived_value` below
is that obligation discharged.
"""

import pytest

from conftest import SCRIPTS, load_script, make_minimal_project, run_py

check = load_script("check")
spine_rules = load_script("spine_rules")

# `kitlib` is a package, not a top-level script, so the ladder comes through
# `check`'s own already-resolved import rather than a second loader path — and
# that is also the assertion that matters: if these tests could reach a DIFFERENT
# ladder object than the selector uses, they would be pinning a copy.
_ladder = check._kitladder

CANARY_PRODUCT = (
    "\n[step:product-canary]\n"
    "command = {py} -c \"print('PRODUCT-CANARY')\"\n"
    "from-stage = DevStg-Reqs\n"
    "layer = product\n"
)

# An ORDINARY new requirement in the SAME phase as the settled one — the C-01
# act exactly as the review words it. Same phase deliberately: a draft in a NEW
# phase is ignored by a different arm of the fold (a phase that has earned
# nothing contributes no opinion), so putting it there would prove the easier
# half and leave the harder one untested.
DRAFTED_SR = (
    'SR-002,Subtraction,SN-001,"The system shall subtract.",'
    '"Realizes SN-001.","sub(3,1) == 2",,M,Test,Drafted\n'
)


def _mature_frame_free(root):
    """A fully decomposed, settled spine that also has NO frame registries.

    Both halves are needed and the second is not tidying. `spine_stage` inserts
    two REPO-GLOBAL frame rungs below every spine rung — `boundary_incomplete`
    (rung 1) and `arch_incomplete` (rung 3) — and each applies only when its
    registry FILE exists (a project that never declares a boundary is not held at
    DevStg-Boundary forever). A scaffold ships `external.toml` and
    `components.toml` carrying no ratified crossing or component, which is
    honestly "the frame is in work", so a scaffold with a perfectly decomposed
    spine still reads DevStg-Boundary and floors to DevStg-Reqs.

    So the adopter shape these tests need is the one that declares no frame:
    remove the two registries and the rungs skip by their own applies-when. That
    is the shape the bar-vs-stage census drove its reachability demonstration
    over, and it is why these fixtures do not simply call make_minimal_project.
    """
    make_minimal_project(root)
    for name in ("external", "components"):
        for suffix in (".toml", ".csv"):
            path = root / "docs" / "requirements" / (name + suffix)
            if path.exists():
                path.unlink()


def _steps_at(stage):
    return check.steps("coverage.json", "smoke", stage, None, None)


def _thresholds(stage="all"):
    return {s[0]: s[3] for s in _steps_at(stage)}


# --- the rule itself ----------------------------------------------------------


def test_every_built_in_threshold_is_a_single_rung_on_the_shared_ladder():
    """The tuple's fourth slot was a SET of bar names and is now ONE rung.

    Pinned structurally because the change is invisible at a call site: a set of
    strings and a string are both truthy, both iterable, and `at_or_above` would
    have happily compared a rung against the first character of a set's repr had
    the two forms ever mixed."""
    for name, threshold in _thresholds().items():
        assert isinstance(threshold, str), name
        assert threshold in _ladder.LADDER_RUNGS, (name, threshold)


def test_selection_is_a_THRESHOLD_and_no_longer_a_membership_set():
    """The one measured behavioral delta of the re-key (the bar-vs-stage census).

    `registry-integrity` was tagged `{DevStg-Reqs}` ALONE — membership, so it
    genuinely did not run at the higher bars. Under an at-or-above rule that set
    is not expressible: the question it answers ("is this registry structurally
    readable?") is relevant at every rung, and a threshold that says so also runs
    it at the top, where `traceability --strict` covers the same ground. The
    duplication is accepted deliberately — it is one cheap read-only pass — and
    recorded here rather than hidden, because it is the single place the
    re-key changed what runs rather than when."""
    thresholds = _thresholds()
    assert thresholds["registry-integrity"] == _ladder.STAGE_NEEDS
    top = _steps_at(_ladder.STAGE_RELEASE)
    selected = {s[0] for s in top if check.at_or_above(_ladder.STAGE_RELEASE, s[3])}
    assert "registry-integrity" in selected
    assert "traceability" in selected


def test_the_floor_and_the_advisory_tier_are_RETIRED_not_merely_unused():
    """Both mechanisms existed for the draft-collapse the effective stage now
    prevents by construction. Left in place they would be dead code that still
    reads `docs/gate` — which is the seam this slice exists to cut — so their
    absence is pinned, exactly as the retired bar constants' is."""
    for gone in (
        "product_floor",
        "floor_plan",
        "floor_notice",
        "window_open",
        "advisory_plan",
        "run_advisory",
        "ADVISORY_EXCLUDE",
        "GATE_FILE",
    ):
        assert not hasattr(check, gone), gone


# --- OI-51's own defect, and its fix ------------------------------------------


def test_the_three_built_in_product_steps_are_REACHABLE_from_a_derived_value(
    scaffold,
):
    """OI-51'S DEFECT, INVERTED INTO ITS FIX.

    `format`/`lint`/`tests+coverage` were tagged `{DevStg-Impl}`, and the OI-30
    D2 ceiling stops the derived BAR at `DevStg-Tests` — so on the retired axis
    those three could not be selected by any derived value at all, on any repo,
    on every push and pull request an adopter runs. The predecessor test pinned
    that as a dormancy and named OI-51 as the ruling that owed the fix.

    The stage axis is not ceilinged. A fully decomposed, settled spine reaches
    `DevStg-Impl` — the threshold itself — so the three select.

    SLICE 3 CHANGED THE RUNG THIS REACHES, AND THE PREVIOUS TEXT PREDICTED IT.
    It read: "That the rung actually reached is Release rather than Impl is
    honest and known: rung 6 is vacant under today's closed Status enum, which
    is why the owner's rule had to be 'in or above' rather than 'in', and slice
    3 re-discriminates the ladder." It did. A settled spine now lands ON the
    threshold rather than above it — the fix is the same size either way, but
    the reading is no longer "nothing in work" for a repo that is being built.
    `at_or_above` is still asserted below, because the RULE is unchanged: the
    owner's "in or above" survives the vacancy closing."""
    _mature_frame_free(scaffold)
    proc = run_py([SCRIPTS / "derive_stage.py", "--root", "."], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    record = check._kitstage.parse((scaffold / "docs" / "stage").read_text("utf-8"))
    assert record["stage"] == _ladder.STAGE_IMPL, record
    assert check.at_or_above(record["stage"], _ladder.STAGE_IMPL)

    listed = run_py(["scripts/check.py", "--list", "--tier", "smoke"], cwd=scaffold)
    assert listed.returncode == 0, listed.stdout + listed.stderr
    for step in ("format", "lint", "tests+coverage"):
        assert step in listed.stdout, listed.stdout

    # THE COUNTERFACTUAL THIS USED TO DRIVE IS NO LONGER RUNNABLE, and saying so
    # is more honest than dropping the paragraph. It regenerated the retired BAR
    # on the same fixture and asserted it read `DevStg-Tests` — one rung short of
    # the three product steps' threshold — which is what made this a fix rather
    # than a fixture that changed. WI-498 slice 5 DELETED that axis, so there is
    # nothing left to compute the counterfactual with. What survives is the pin
    # that the deletion happened (a re-introduced bar would restore the hazard)
    # plus the threshold itself.
    assert not hasattr(spine_rules, "compute"), "the bar derivation is retired"
    assert _thresholds()["format"] == _ladder.STAGE_IMPL


def test_one_drafted_row_cannot_drop_a_single_selected_check(scaffold):
    """THE C-01 REGRESSION SCENARIO, DRIVEN AT THE SELECTION LEVEL.

    The review's words: *"start with a mature repository, add one Drafted row,
    and assert that all established product checks remain in the plan."* The
    predecessor drove it against the floor; this drives it against selection
    itself, which is strictly more than the floor claimed — the floor restored
    PRODUCT steps only, and here nothing at all is lost, process steps included.

    The proof obligation is two-sided, and the second side is what stops this
    from being a tautology: something must be shown to have genuinely MOVED when
    the draft landed. A fixture where nothing moved would pass this test while
    proving nothing.

    THE MOVING SIDE CHANGED CARRIER AT WI-498 slice 5. It was the derived BAR,
    which the draft collapsed from `DevStg-Tests` to `DevStg-Reqs`; that axis is
    now deleted. The `live-stage` field carries the same evidence on the
    surviving axis — the unfiltered reading, where a draft DOES show — so the
    two-sided proof is intact and now runs entirely within one vocabulary. That
    the settled `stage` and the live reading disagree here is the C-01 fix
    itself, stated as a measurement rather than as a claim."""
    docs = scaffold / "docs"
    _mature_frame_free(scaffold)
    stack = docs / "stack.ini"
    stack.write_text(
        stack.read_text(encoding="utf-8") + CANARY_PRODUCT, encoding="utf-8"
    )

    def regenerate():
        proc = run_py([SCRIPTS / "derive_stage.py", "--root", "."], cwd=scaffold)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return check._kitstage.parse((docs / "stage").read_text("utf-8"))

    def plan_names():
        proc = run_py(["scripts/check.py", "--list", "--tier", "smoke"], cwd=scaffold)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return {
            line.split()[1]
            for line in proc.stdout.splitlines()
            if line.strip().startswith("- ")
        }

    # 1. MATURE: a fully decomposed settled chain.
    stage_before = regenerate()
    before = plan_names()
    assert stage_before["stage"] == _ladder.STAGE_IMPL, stage_before
    assert {"product-canary", "traceability", "format"} <= before, before

    # 2. ONE DRAFTED ROW — an ordinary new requirement, nothing else changed.
    srs = docs / "requirements" / "system-requirements.csv"
    srs.write_text(srs.read_text(encoding="utf-8") + DRAFTED_SR, encoding="utf-8")
    stage_after = regenerate()

    # 2a. THE CONTROL: the draft really did move something. Without this the
    #     claim below could pass on a fixture where nothing ever moved.
    assert stage_before["live-stage"] == _ladder.STAGE_IMPL, stage_before
    assert stage_after["live-stage"] == _ladder.STAGE_REQS, stage_after

    # 2b. THE CLAIM: the effective stage did not move, so the plan did not.
    assert stage_after["stage"] == _ladder.STAGE_IMPL, stage_after
    assert plan_names() == before


# --- the declared per-step threshold, and its migration -----------------------


def test_a_declared_step_names_its_rung_with_from_stage(scaffold, capsys):
    make_minimal_project(scaffold)
    stack = scaffold / "docs" / "stack.ini"
    stack.write_text(
        stack.read_text(encoding="utf-8") + CANARY_PRODUCT, encoding="utf-8"
    )
    profile = check.load_profile(stack)
    declared = {s[0]: s[3] for s in check.extra_steps(profile, {"py": "python"})}
    assert declared["product-canary"] == _ladder.STAGE_REQS


def test_the_retired_gates_list_translates_to_the_rung_it_EFFECTIVELY_meant(
    tmp_path, capsys
):
    """`gates = DevStg-Tests` becomes `from-stage = DevStg-Impl`, not
    `DevStg-Arch`, and the difference is the whole reason the translation is a
    table rather than a span lookup.

    A `gates =` list named BARS. The bar was a MIN over every in-scope row, so
    `DevStg-Tests` was reached only by a spine already fully decomposed and TC'd
    — which is the DevStg-Impl RUNG, not the DevStg-Arch rung that merely opens
    that bar's span. Translating to the span's floor would silently start running
    an adopter's step three rungs early, on a repo that has not built what the
    step grades."""
    ini = tmp_path / "stack.ini"
    ini.write_text(
        "[step:legacy]\ncommand = {py} -c pass\ngates = DevStg-Tests DevStg-Impl\n"
        "[step:legacy-low]\ncommand = {py} -c pass\ngates = DevStg-Reqs\n",
        encoding="utf-8",
    )
    profile = check.load_profile(ini)
    check._LEGACY_GATES_WARNED.clear()
    declared = {s[0]: s[3] for s in check.extra_steps(profile, {"py": "python"})}
    assert declared["legacy"] == _ladder.STAGE_IMPL
    assert declared["legacy-low"] == _ladder.STAGE_NEEDS
    notice = capsys.readouterr().err
    assert "RETIRED `gates =`" in notice
    assert "from-stage = DevStg-Impl" in notice


def test_declaring_both_spellings_fails_loudly(tmp_path):
    ini = tmp_path / "stack.ini"
    ini.write_text(
        "[step:both]\ncommand = {py} -c pass\ngates = DevStg-Impl\n"
        "from-stage = DevStg-Reqs\n",
        encoding="utf-8",
    )
    profile = check.load_profile(ini)
    with pytest.raises(SystemExit) as exc:
        check.extra_steps(profile, {"py": "python"})
    assert "both `from-stage` and the retired `gates`" in str(exc.value)


def test_an_unknown_from_stage_value_fails_loudly(tmp_path):
    ini = tmp_path / "stack.ini"
    ini.write_text(
        "[step:bad]\ncommand = {py} -c pass\nfrom-stage = DevStg-Nope\n",
        encoding="utf-8",
    )
    profile = check.load_profile(ini)
    with pytest.raises(SystemExit) as exc:
        check.extra_steps(profile, {"py": "python"})
    assert "from-stage is 'DevStg-Nope'" in str(exc.value)


# --- the flag surface ---------------------------------------------------------


def test_the_stage_cleared_spelling_warns_and_gate_stays_silent(capsys):
    """The two prior spellings get DIFFERENT postures, and the asymmetry is the
    ruling rather than an oversight: `--gate` is a flag NAME an adopter's
    pipeline passes literally and the word was never retired, while
    `--stage-cleared` makes a CLAIM about the axis — that the value is a bar
    being cleared — which is precisely the reading OI-51 retires."""
    assert check._warn_retired_flag_spelling(["--gate", "all"]) is False
    assert check._warn_retired_flag_spelling(["--stage", "DevStg-Impl"]) is False
    assert capsys.readouterr().err == ""
    assert check._warn_retired_flag_spelling(["--stage-cleared", "DevStg-Impl"])
    assert check._warn_retired_flag_spelling(["--stage-cleared=DevStg-Impl"])
    err = capsys.readouterr().err
    assert err.count("RETIRED bar reading") == 2


@pytest.mark.parametrize("flag", ["--stage", "--stage-cleared", "--gate"])
def test_all_three_spellings_still_select_the_same_plan(scaffold, flag):
    make_minimal_project(scaffold)
    proc = run_py(
        ["scripts/check.py", flag, "DevStg-Reqs", "--list", "--tier", "smoke"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Plan at stage DevStg-Reqs" in proc.stdout


def test_a_retired_value_alias_resolves_BY_MEANING_and_says_so(scaffold):
    """A retired tag translates to the rung a repo at that BAR had REACHED —
    never to the same-spelled rung.

    THIS TEST PINNED THE DEFECT UNTIL THE WI-498 CLOSE (ROUND-OPUS 8). It
    asserted `G2` → `DevStg-Tests`, which is the SPELLING;  check_vocab: allow
    the bar was a MIN
    over every in-scope row, so the `DevStg-Tests` bar was reached only by a
    spine already fully decomposed and TC'd — the `DevStg-Impl` RUNG, three
    above the shared word. `_LEGACY_BAR_THRESHOLD` had that rule written down
    for `gates =` lists; `RETIRED_STAGE_ALIASES` did not apply it, and this
    test held the disagreement in place.

    What it cost, and why the assertion below is the load-bearing one: at the
    spelling reading `--gate G2` selected 12 steps  check_vocab: allow
    where the arrival reading
    selects 26, silently dropping `traceability`, `tests+coverage`, `lint`,
    `format` and ten others. An adopter's CI passing the tag literally — the
    exact case the silent-`--gate` concession exists to protect — stayed green
    while quietly stopping most of its checks."""
    make_minimal_project(scaffold)
    proc = run_py(
        # The retired tag is the ARGUMENT under test, not a live citation.
        [
            "scripts/check.py",
            "--stage",
            "G2",  # check_vocab: allow
            "--list",
            "--tier",
            "smoke",
        ],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RETIRED gate vocabulary" in proc.stderr
    assert "Plan at stage DevStg-Impl" in proc.stdout
    # The warning must SAY the value moved and that the plan moved with it —
    # the old text reported only the re-reading, so a pipeline could shrink by
    # fourteen steps behind one line of reassurance.
    assert "NOT the same-spelled rung" in proc.stderr, proc.stderr
    # ...and the steps the spelling reading dropped are genuinely back.
    assert "format" in proc.stdout


# --- the reader seam ----------------------------------------------------------


def test_the_stage_is_read_through_the_common_reader_not_off_a_stale_cache(
    scaffold,
):
    """The plan is selected from a value the reader VERIFIED, not from whatever
    the committed file happens to say — the ruled plan §3 contract, observed
    from the selector's side.

    Driven by editing a declared derivation input and NOT regenerating: the
    fingerprint misses, `resolve_stage` derives fresh through the subprocess
    deriver, and the plan follows the tree rather than the cache. This is the
    branch-lane window closed by construction, since `derived-stage` stands down
    on a claimed branch and could not have caught it."""
    docs = scaffold / "docs"
    _mature_frame_free(scaffold)
    for script in ("spine_rules.py", "derive_stage.py"):
        assert run_py([SCRIPTS / script, "--root", "."], cwd=scaffold).returncode == 0
    recorded = (docs / "stage").read_text(encoding="utf-8")
    assert "stage = DevStg-Impl" in recorded

    srs = docs / "requirements" / "system-requirements.csv"
    srs.write_text(srs.read_text(encoding="utf-8") + DRAFTED_SR, encoding="utf-8")

    proc = run_py(["scripts/check.py", "--list", "--tier", "smoke"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # The effective stage is draft-excluded, so the headline does not move —
    # what this proves is that the file was NOT trusted blindly: it is byte
    # identical afterwards (readers never write) while the fingerprint missed.
    assert (docs / "stage").read_text(encoding="utf-8") == recorded
    assert "Plan at stage DevStg-Impl" in proc.stdout
