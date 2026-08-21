"""The authoring-time stage-decrease rule (`derive_stage.phase_rule_findings`).

WI-498 slice 3, ruled plan `docs/plans/2026-08-21-stage-unification-plan.md` §4
with the owner's answers §6.1 (phase stays DERIVED; the decrease rule is an
AUTHORING-TIME check, not a stored counter) and §6.2 (the exemption is EXACTLY
the one permutation `DevStg-LLReqs -> DevStg-Arch`, the permitted decomposition
cycle).

THE RULE: a spine edit that LOWERS the effective stage must surface as a phase
change. Every row the edit added or re-statused has to carry a `Phase` tag that
is not the phase the settled work was standing in — a new (higher) phase, or an
already-open lower one.

These are real git repos, because the rule's before-state IS `HEAD`. That puts
this module in the subprocess/scaffold-heavy tier (`conftest.SLOW_MODULES`)
beside `test_derive_stage`, whose fixtures it borrows.
"""

import subprocess

import pytest
from conftest import ROOT, SCRIPTS, load_script, pin_autocrlf, run_py

from kitlib import ladder

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
NEEDS = "# Stakeholder needs\n\n## SN-001 — A demo need [Approved]\n\nBody.\n"


def _sr(sid, phase, status="Approved"):
    return '{},T,SN-001,"r","why","ac",,M,Test,{},{}\n'.format(sid, status, phase)


def _llr(lid, sr, phase, status="Approved"):
    return '{},{},Adder,src/demo,add,"d",(see TC),{},{}\n'.format(
        lid, sr, status, phase
    )


def _tc(tid, verifies, phase, status="Approved"):
    return '{},{},Unit,m,Smoke,"a=1","e",Yes,tests/test_demo.py::t,{},{}\n'.format(
        tid, verifies, status, phase
    )


def _git(root, *args):
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.fixture()
def repo(tmp_path):
    """A committed, FRAME-FREE spine repo.

    Frame-free (no `external.toml` / `components.toml`) for the reason
    `test_derive_stage._no_frame` records and slice 2's finding sharpened: the
    two inserted rungs are repo-global and sit BELOW every spine rung, so a
    scaffold's blank-but-present boundary registry pins every phase at
    `DevStg-Boundary` and no spine-rung difference is observable at all. The
    exemption test below re-introduces a component registry precisely because
    the `DevStg-Arch` rung it must produce is derived from one."""
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)
    (tmp_path / "docs" / "requirements" / "stakeholder-needs.md").write_text(
        NEEDS, encoding="utf-8", newline="\n"
    )
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "T")
    _git(tmp_path, "config", "commit.gpgsign", "false")
    pin_autocrlf(tmp_path)
    return tmp_path


def _write(root, srs="", llrs="", tcs=""):
    req = root / "docs" / "requirements"
    (req / "system-requirements.csv").write_text(
        SRS_H + srs, encoding="utf-8", newline="\n"
    )
    (req / "low-level-requirements.csv").write_text(
        LLRS_H + llrs, encoding="utf-8", newline="\n"
    )
    (root / "docs" / "test" / "test-cases.csv").write_text(
        TCS_H + tcs, encoding="utf-8", newline="\n"
    )


def _commit(root, message="state"):
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", message)


def _settled(sr, phase):
    """One phase whose single SR is Approved, decomposed and verified — the
    shape that reads `DevStg-Impl` since slice 3 re-discriminated the ladder."""
    n = sr.split("-")[1]
    return (_sr(sr, phase), _llr("LLR-" + n, sr, phase), _tc("TC-" + n, sr, phase))


def _stage(root):
    return DS._effective(DS.derive_gate.load_spine(root / "docs"))


# --- the baseline the four directions move from -------------------------------
def test_the_committed_baseline_is_a_settled_IMPL_spine(repo):
    srs, llrs, tcs = _settled("SR-001", "1")
    _write(repo, srs, llrs, tcs)
    _commit(repo)
    assert _stage(repo) == ladder.STAGE_IMPL
    assert DS.phase_rule_findings(repo) == []


# --- DIRECTION 1: a stage-lowering edit with NO new phase tag FIRES ------------
def test_a_lowering_edit_in_the_STANDING_phase_FIRES(repo):
    """The rule's whole purpose: scope added to the phase you are standing in,
    which drops the reading, with nothing saying the scope moved."""
    srs, llrs, tcs = _settled("SR-001", "1")
    _write(repo, srs, llrs, tcs)
    _commit(repo)

    # a second requirement in the SAME phase, ratified, not yet decomposed
    _write(repo, srs + _sr("SR-002", "1"), llrs, tcs)
    assert _stage(repo) == ladder.STAGE_LLREQS  # Impl -> LLReqs, a real decrease

    findings = DS.phase_rule_findings(repo)
    assert len(findings) == 1, findings
    assert "SR-002" in findings[0]
    assert "DevStg-Impl -> DevStg-LLReqs" in findings[0]
    assert "new phase (2)" in findings[0]  # the remedy it names


# --- DIRECTION 2: the SAME edit, carrying a new phase tag, PASSES --------------
def test_the_same_edit_with_a_NEW_phase_tag_PASSES(repo):
    """Identical decrease, identical row, one cell different. That the two tests
    differ ONLY in the `Phase` cell is the point — it is what shows the rule
    grades the phase signal and not the decrease."""
    srs, llrs, tcs = _settled("SR-001", "1")
    _write(repo, srs, llrs, tcs)
    _commit(repo)

    _write(repo, srs + _sr("SR-002", "2"), llrs, tcs)
    assert _stage(repo) == ladder.STAGE_LLREQS  # the same decrease
    assert DS.phase_rule_findings(repo) == []


def test_an_ALREADY_OPEN_LOWER_phase_also_satisfies_the_rule(repo):
    """The plan's second permitted answer: "a NEW (or already-open lower) phase
    tag". Work returning to an earlier phase is a declared scope move too."""
    srs = _settled("SR-001", "1")[0] + _settled("SR-002", "2")[0]
    llrs = _settled("SR-001", "1")[1] + _settled("SR-002", "2")[1]
    tcs = _settled("SR-001", "1")[2] + _settled("SR-002", "2")[2]
    _write(repo, srs, llrs, tcs)
    _commit(repo)
    assert _stage(repo) == ladder.STAGE_IMPL

    # standing phase is 2; the new row goes back into the open phase 1
    _write(repo, srs + _sr("SR-003", "1"), llrs, tcs)
    assert _stage(repo) == ladder.STAGE_LLREQS
    assert DS.phase_rule_findings(repo) == []


# --- DIRECTION 3: the ONE exempt permutation passes with no phase tag ----------
def test_the_LLREQS_to_ARCH_decrease_is_EXEMPT(repo):
    """Owner answer §6.2: exactly the one permutation `LLReqs -> Arch`, the
    PERMITTED DECOMPOSITION CYCLE. Architecture rework surfaced by breaking a
    requirement down is within-phase churn; any deeply decomposed problem would
    otherwise run the phase counter up.

    Driven through the COMPONENT registry, because that is what the Arch rung
    reads — and it is why the rule's before-state re-reads the whole frame at
    HEAD rather than pinning it to the live tree. With the frame held constant
    this transition is unreachable and the exemption would be dead code."""
    req = repo / "docs" / "requirements"
    cmp_h = "CMP-ID,Name,Status,Standing\n"
    (req / "components.csv").write_text(
        cmp_h + "CMP-001,Core,Approved,\n", encoding="utf-8", newline="\n"
    )
    # an SR with no LLR holds the spine at LLReqs; the partition is settled
    _write(repo, _sr("SR-001", "1"), "", _tc("TC-001", "SR-001", "1"))
    _commit(repo)
    assert _stage(repo) == ladder.STAGE_LLREQS

    # THE PARTITION RECORDS A GAP, dropping the reading exactly one rung, to
    # Arch. What does NOT work here is worth stating, because it is rung 3's own
    # headline behaviour: a newly *Drafted* CMP row — the "self-reporting
    # recursion" `arch_incomplete`'s docstring describes, where identifying a
    # sub-component drops the stage with nobody deciding to — is filtered out of
    # the SETTLED fold by the same draft-exclusion that hides a drafted spine
    # row, so it cannot move the effective stage at all. A settled row honestly
    # reporting `has-gap` is the reachable route.
    (req / "components.csv").write_text(
        cmp_h + "CMP-001,Core,Approved,has-gap\n", encoding="utf-8", newline="\n"
    )
    assert _stage(repo) == ladder.STAGE_ARCH
    assert DS.phase_rule_findings(repo) == []


# --- DIRECTION 4: a decrease of another shape FIRES ---------------------------
def test_a_TWO_RUNG_decrease_that_merely_ENDS_at_Arch_is_NOT_exempt(repo):
    """The exemption is a PAIR, not a predicate over the Arch rung (§6.2 declined
    a wider Arch-tier exemption). A drop from Impl that happens to land on Arch
    is not the decomposition cycle and must still be declared."""
    req = repo / "docs" / "requirements"
    cmp_h = "CMP-ID,Name,Status,Standing\n"
    (req / "components.csv").write_text(
        cmp_h + "CMP-001,Core,Approved,\n", encoding="utf-8", newline="\n"
    )
    srs, llrs, tcs = _settled("SR-001", "1")
    _write(repo, srs, llrs, tcs)
    _commit(repo)
    assert _stage(repo) == ladder.STAGE_IMPL

    # the partition records a gap AND a same-phase requirement arrives undecomposed
    (req / "components.csv").write_text(
        cmp_h + "CMP-001,Core,Approved,has-gap\n", encoding="utf-8", newline="\n"
    )
    _write(repo, srs + _sr("SR-002", "1"), llrs, tcs)
    assert _stage(repo) == ladder.STAGE_ARCH  # Impl -> Arch, three rungs

    findings = DS.phase_rule_findings(repo)
    assert len(findings) == 1, findings
    assert "SR-002" in findings[0]
    assert "DevStg-Impl -> DevStg-Arch" in findings[0]


def test_a_REDRAFTED_child_in_the_standing_phase_FIRES(repo):
    """The OTHER shape that actually lowers the effective stage, and the reason
    the trigger set is "added, or Status moved" rather than the plan's literal
    "newly drafted". Redrafting an LLR removes it from the settled fold, which
    leaves its SR undecomposed."""
    srs, llrs, tcs = _settled("SR-001", "1")
    _write(repo, srs, llrs, tcs)
    _commit(repo)

    _write(repo, srs, _llr("LLR-001", "SR-001", "1", status="Drafted"), tcs)
    assert _stage(repo) == ladder.STAGE_LLREQS

    findings = DS.phase_rule_findings(repo)
    assert len(findings) == 1, findings
    assert "LLR-001" in findings[0]
    assert "Approved -> Drafted" in findings[0]


# --- the measurement that shaped the trigger set ------------------------------
def test_a_NEW_DRAFT_cannot_lower_the_effective_stage_AT_ALL(repo):
    """MEASURED, and it is why the rule does not key on the plan's literal words.

    Plan §4 says "a newly drafted/redrafted row would DECREASE the effective
    stage". Slice 1 excludes drafts from the settled fold, so the DRAFTED half is
    inert BY CONSTRUCTION — in both directions, the standing phase and a brand
    new one. A rule that triggered only on newly drafted rows could never fire.

    This is not a defect in either slice: it is slice 1's C-01 fix working, and
    recording it here stops a future reader from "restoring" the literal wording
    and shipping a rule with no reachable trigger."""
    srs, llrs, tcs = _settled("SR-001", "1")
    _write(repo, srs, llrs, tcs)
    _commit(repo)
    before = _stage(repo)

    for phase in ("1", "2"):  # the standing phase, then a brand-new one
        _write(repo, srs + _sr("SR-002", phase, status="Drafted"), llrs, tcs)
        assert _stage(repo) == before, phase
        assert DS.phase_rule_findings(repo) == []


# --- the degrade, and the CLI contract ----------------------------------------
def test_without_git_the_rule_has_NOTHING_TO_SAY(tmp_path):
    """The silent-no-op degrade every two-tree rule in the kit shares: no HEAD
    means no before-state, and a rule that cannot see the past reports nothing
    rather than complaining about it."""
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)
    (tmp_path / "docs" / "requirements" / "stakeholder-needs.md").write_text(
        NEEDS, encoding="utf-8", newline="\n"
    )
    _write(tmp_path, *_settled("SR-001", "1"))
    assert DS.phase_rule_findings(tmp_path) == []


def test_the_CLI_is_WARN_FIRST_and_STRICT_promotes(repo):
    """Tier decision, pinned: findings WARN and exit 0; `--strict` FAILs and
    exits 1. New rules arm warn-first here unless a ruling says otherwise, and
    OI-51 ruled that the rule EXISTS, not that it blocks a commit on day one.
    The promotion is a call-site change, not a second predicate."""
    srs, llrs, tcs = _settled("SR-001", "1")
    _write(repo, srs, llrs, tcs)
    _commit(repo)
    _write(repo, srs + _sr("SR-002", "1"), llrs, tcs)

    warn = run_py(
        [SCRIPTS / "derive_stage.py", "--root", repo, "--phase-rule"], cwd=repo
    )
    assert warn.returncode == 0, warn.stdout + warn.stderr
    assert "WARN - SR-002" in warn.stdout

    strict = run_py(
        [SCRIPTS / "derive_stage.py", "--root", repo, "--phase-rule", "--strict"],
        cwd=repo,
    )
    assert strict.returncode == 1
    assert "FAIL - SR-002" in strict.stdout


def test_THIS_repo_does_not_fire_the_rule(repo):
    """The kit's own tree, measured rather than assumed (the slice brief's
    migration question). No seeded allowlist was needed: this repo's effective
    stage has not decreased, so the rule has nothing to fire on. Its 15 Drafted
    rows are all phase 5 and — per the test above — cannot lower the reading
    anyway, and the two repo-global frame rungs pin every phase at
    `DevStg-Arch` while the partition is in work."""
    del repo  # this test is about ROOT, and takes the fixture only to stay in tier
    assert DS.phase_rule_findings(ROOT) == []
