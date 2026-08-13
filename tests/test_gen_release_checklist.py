"""gen_release_checklist.py: the DevStg-Release human sign-off record (M-17).

The script collects the human-verified items — Demonstration/Manual/Inspection
SRs, release-tier + manual TCs, provided IFs, PB budgets — into a tick-box
checklist. These tests pin the behaviors the shipped reference CI leans on:
the --phase scope filter (incl. the foundation-min-phase-never-deferred rule),
TC-cites-LLR-only phase resolution, blank-`Automated`-counts-as-manual, the
--version output routing, and the empty/absent-registry degradation.
"""

from conftest import SCRIPTS, run_py, use_legacy_spine_carrier

SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase,Area\n"
)
LLR_HEADER = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component,Phase\n"
)
TC_HEADER = "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status,Phase\n"


def sr_row(rid, title, phase="", verification="Demonstration", status="Verified"):
    return '{},{},SN-001,"The system shall {}.","Why.","Observable.",,M,{},{},{},\n'.format(
        rid, title, title.lower(), verification, status, phase
    )


def llr_row(rid, sr_refs):
    return '{},{},Decomposition,src/mod,func,"Detail.",(see TC),Implemented,,\n'.format(
        rid, sr_refs
    )


def tc_row(rid, verifies, tier="Full", automated="No"):
    return '{},{},Unit,exercise it by hand,{},"p=1","Meets the cited AcceptanceCriteria",{},,Draft,\n'.format(
        rid, verifies, tier, automated
    )


def write_srs(root, *rows):
    # These fixtures write the LEGACY carrier onto a scaffold that now ships the
    # TOML one, and `spine_carrier.resolve` refuses both homes at once rather
    # than picking by precedence — so the scaffolded counterpart goes first
    # (conftest.use_legacy_spine_carrier states the reasoning).
    use_legacy_spine_carrier(root)
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + "".join(rows), encoding="utf-8"
    )


def write_llrs(root, *rows):
    use_legacy_spine_carrier(root)
    (root / "docs" / "requirements" / "low-level-requirements.csv").write_text(
        LLR_HEADER + "".join(rows), encoding="utf-8"
    )


def write_tcs(root, *rows):
    use_legacy_spine_carrier(root)
    (root / "docs" / "test" / "test-cases.csv").write_text(
        TC_HEADER + "".join(rows), encoding="utf-8"
    )


def checklist(root):
    return (root / "docs" / "release-checklist.md").read_text(encoding="utf-8")


def gen(root, *extra):
    return run_py(["scripts/gen_release_checklist.py", *extra], cwd=root)


# --- (a) --phase scoping + the min-phase-never-deferred rule ------------------


def test_phase_filter_drops_deferred_and_keeps_foundation(scaffold):
    write_srs(
        scaffold,
        sr_row("SR-001", "Foundation capability", phase="1"),
        sr_row("SR-002", "Deferred capability", phase="2"),
    )
    proc = gen(scaffold, "--phase", "1")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = checklist(scaffold)
    assert "SR-001" in text
    assert "SR-002" not in text, "a deferred-phase SR must leave the checklist"
    assert "human-SR=1" in proc.stdout
    # The foundation (minimum) phase is never phase-deferred: a --phase naming
    # only the LATER phase still keeps the foundation SR on the checklist.
    proc = gen(scaffold, "--phase", "2")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = checklist(scaffold)
    assert "SR-001" in text, "the foundation SR must survive any --phase"
    assert "SR-002" in text
    assert "human-SR=2" in proc.stdout


def test_blank_phase_rows_are_in_scope_under_any_phase(scaffold):
    # A blank Phase means "every phase" — the row never drops out.
    write_srs(scaffold, sr_row("SR-001", "Unphased capability", phase=""))
    proc = gen(scaffold, "--phase", "7")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SR-001" in checklist(scaffold)


# --- (b) TC citing only an LLR resolves through the parent SR's phase ---------


def test_tc_citing_only_an_llr_follows_the_parent_sr_phase(scaffold):
    write_srs(
        scaffold,
        sr_row("SR-001", "In scope", phase="1", verification="Test"),
        sr_row("SR-002", "Deferred", phase="2", verification="Test"),
    )
    write_llrs(scaffold, llr_row("LLR-001", "SR-001"), llr_row("LLR-002", "SR-002"))
    write_tcs(
        scaffold,
        tc_row("TC-001", "LLR-001"),  # cites ONLY the LLR, never the SR
        tc_row("TC-002", "LLR-002"),
    )
    proc = gen(scaffold, "--phase", "1")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = checklist(scaffold)
    assert "TC-001" in text, "a TC under an in-scope SR (via its LLR) must appear"
    assert "TC-002" not in text, "a TC under a deferred SR must not"
    assert "manual-TC=1" in proc.stdout


# --- (c) blank Automated counts as a manual item ------------------------------


def test_blank_automated_lands_on_the_human_checklist(scaffold):
    write_srs(scaffold, sr_row("SR-001", "Cap", verification="Test"))
    write_tcs(
        scaffold,
        tc_row("TC-001", "SR-001", tier="Full", automated=""),  # unclassified
        tc_row("TC-002", "SR-001", tier="Full", automated="Yes"),
    )
    proc = gen(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = checklist(scaffold)
    assert "TC-001" in text, "an unclassified test must not silently drop off"
    assert "TC-002" not in text, "an automated full-tier TC is not a manual item"
    assert "manual-TC=1" in proc.stdout


# --- (d) --version routes under docs/releases/ --------------------------------


def test_version_writes_the_release_stamped_copy(scaffold):
    proc = gen(scaffold, "--version", "1.2.3")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = scaffold / "docs" / "releases" / "checklist-1.2.3.md"
    assert out.exists(), "--version must write docs/releases/checklist-<X>.md"
    text = out.read_text(encoding="utf-8")
    assert "# Release Checklist — 1.2.3" in text
    assert "checklist-1.2.3.md" in proc.stdout


# --- (e) empty/absent registries degrade sanely -------------------------------


def test_absent_registries_still_produce_a_sane_checklist(tmp_path):
    # No docs/ at all: every input degrades to empty; the script writes a
    # checklist carrying the honest empty-section placeholders and exits 0.
    proc = run_py([SCRIPTS / "gen_release_checklist.py"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SN=0 human-SR=0 manual-TC=0 IF=0 PB=0" in proc.stdout
    text = (tmp_path / "docs" / "release-checklist.md").read_text(encoding="utf-8")
    assert "(no stakeholder needs registered)" in text
    assert "every requirement is automated" in text
    assert "no release-tier or manual test cases" in text


def test_fresh_scaffold_example_rows_do_not_count(scaffold):
    # A fresh scaffold carries only the -000 example rows — ignored like
    # everywhere else in the kit, so the counts are all zero and the run is
    # green out of the box.
    proc = gen(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SN=0 human-SR=0 manual-TC=0 IF=0 PB=0" in proc.stdout
