"""The plan step's filing on a real lane (WI-913): the plan critique's brief,
filing each critique beside the plan, and the pass record at the cap.

`review_brief.py plan-file` files a critique bound to the lane commit it
judged, and from a later commit writes the pass record; `critique --plan`
renders the critic's brief over the committed plan and its coverage report.
Each refusal exits 2 and writes nothing. They spawn git and the coverage
gate, so this module is in `tests/conftest.py`'s `SLOW_MODULES`; the
in-process pin is `test_plan_pass.py`.
"""

import pytest
from conftest import ROOT
from test_plan_gate import (
    BRANCH,
    PLAN,
    WI,
    commit,
    critique_text,
    git,
    make_lane,
    rb,
    staged,
    write,
)

from kitlib import dispute as kdispute
from kitlib import plan_pass as pp

RUBRIC = "docs/rubrics/plan-decomposition.md"
MAJOR = "- [MAJOR] docs/plans/WI-950/plan.md:5 -> P2 has no test -> add one -> @owner"
MINOR = "- [MINOR] docs/plans/WI-950/plan.md:5 -> wording -> reword -> @owner"
VERDICT = "docs/reviews/wi-950/003-ADJUDICATE-abc1234.md"
FINDINGS = "docs/reviews/wi-950/002-DISPUTE-findings.toml"
MAJOR2 = (
    "- [BLOCKER] docs/plans/WI-950/plan.md:6 -> P1 is unsolvable -> split -> @owner"
)


def planned(tmp_path, plan=PLAN):
    _trunk, lane = make_lane(tmp_path)
    write(lane, RUBRIC, (ROOT / RUBRIC).read_text(encoding="utf-8"))
    write(lane, pp.plan_path(WI), plan)
    return lane, commit(lane, "plan")


def file_cli(lane, verdict_path, sha):
    argv = ["plan-file", "--root", str(lane), "--wi", WI]
    return rb.main(argv + ["--critique", str(verdict_path), "--sha", sha])


def clean(lane):
    return git(lane, "status", "--porcelain")


# --- filing a critique --------------------------------------------------------------


@pytest.mark.parametrize(
    "shape",
    ["unbound", "malformed", "count-mismatched", "changes-without-findings"],
)
def test_a_critique_outside_the_verdict_format_is_refused_and_nothing_is_written(
    tmp_path, shape
):
    lane, sha = planned(tmp_path)
    text = {
        "unbound": critique_text("f" * 40),
        "malformed": "Reviewed: {}\n\nLooks fine.\n".format(sha),
        "count-mismatched": critique_text(sha, findings=[MAJOR]).replace(
            "findings=1", "findings=2"
        ),
        "changes-without-findings": critique_text(sha, "CHANGES-REQUESTED"),
    }[shape]
    verdict = write(tmp_path, "scratch/v.md", text)
    assert file_cli(lane, verdict, sha) == 2
    assert clean(lane) == ""


@pytest.mark.parametrize("delta", ["", "DELTA: beyond\n"])
def test_a_plan_with_a_missing_or_beyond_delta_is_never_filed(tmp_path, delta):
    lane, sha = planned(tmp_path, PLAN.replace("DELTA: none\n", delta))
    verdict = write(tmp_path, "scratch/v.md", critique_text(sha))
    assert file_cli(lane, verdict, sha) == 2
    assert clean(lane) == ""


def test_a_filed_critique_exits_zero_and_writes_only_its_record(tmp_path):
    lane, sha = planned(tmp_path)
    verdict = write(tmp_path, "scratch/v.md", critique_text(sha))
    assert file_cli(lane, verdict, sha) == 0
    assert clean(lane) == "?? docs/plans/WI-950/critique-1.md"


# --- the pass form -------------------------------------------------------------------


def test_the_pass_form_refuses_while_head_lacks_the_critique_it_cites(tmp_path):
    lane, sha = planned(tmp_path)
    rb.file_plan_critique(lane, WI, critique_text(sha), sha)
    argv = ["plan-file", "--root", str(lane), "--wi", WI, "--pass"]
    assert rb.main(argv) == 2
    assert not (lane / pp.record_path(WI)).exists()
    commit(lane, "critique")
    assert rb.main(argv) == 0
    assert staged(lane) == []


def test_the_pass_form_reads_a_committed_critique_through_line_ending_conversion(
    tmp_path,
):
    # Fable REVIEW-B F1 (round 2): a re-checkout under core.autocrlf=true
    # leaves CRLF in the working tree of a committed critique; HEAD holds it
    # all the same. A real uncommitted edit still refuses.
    lane, sha = planned(tmp_path)
    rb.file_plan_critique(lane, WI, critique_text(sha), sha)
    commit(lane, "critique")
    git(lane, "config", "core.autocrlf", "true")
    path = lane / pp.critique_path(WI, 1)
    filed = path.read_bytes()
    path.write_bytes(filed.replace(b"Verified: the plan.", b"Verified: edited."))
    with pytest.raises(rb.BriefError, match="HEAD does not hold"):
        rb.write_pass(lane, WI)
    path.write_bytes(filed.replace(b"\n", b"\r\n"))
    assert rb.write_pass(lane, WI).is_file()


def test_a_plan_the_coverage_gate_fails_never_passes(tmp_path):
    lane, sha = planned(tmp_path, PLAN.replace("| D2 |", "| SR-001 |"))
    rb.file_plan_critique(lane, WI, critique_text(sha), sha)
    commit(lane, "critique")
    with pytest.raises(rb.BriefError, match="coverage gate"):
        rb.write_pass(lane, WI)
    assert not (lane / pp.record_path(WI)).exists()


def test_a_minor_only_change_request_passes(tmp_path):
    lane, sha = planned(tmp_path)
    text = critique_text(sha, "CHANGES-REQUESTED", [MINOR])
    rb.file_plan_critique(lane, WI, text, sha)
    commit(lane, "critique")
    assert rb.write_pass(lane, WI).is_file()
    assert staged(lane) == []


def test_a_first_change_request_allows_one_revision_and_never_passes(tmp_path):
    lane, sha = planned(tmp_path)
    rb.file_plan_critique(
        lane, WI, critique_text(sha, "CHANGES-REQUESTED", [MAJOR]), sha
    )
    commit(lane, "critique")
    with pytest.raises(rb.BriefError, match="revise once"):
        rb.write_pass(lane, WI)


def second_critique(tmp_path, second):
    """`(lane, its text)`: a plan through its first critique (one MAJOR), its
    one revision, and a filed second critique requesting changes on the
    `second` findings."""
    lane, sha = planned(tmp_path)
    rb.file_plan_critique(
        lane, WI, critique_text(sha, "CHANGES-REQUESTED", [MAJOR]), sha
    )
    commit(lane, "critique 1")
    revised = PLAN.replace("| D2 | intra-module", "| D2; F1 | intra-module")
    write(lane, pp.plan_path(WI), revised)
    sha2 = commit(lane, "the one revision")
    text = critique_text(sha2, "CHANGES-REQUESTED", list(second))
    rb.file_plan_critique(lane, WI, text, sha2)
    commit(lane, "critique 2")
    return lane, text


def cap(
    tmp_path,
    ruling="RULING: F1 DISMISS refuted the plan has the test",
    outcome="accepted",
    second=(MAJOR,),
):
    """A plan through both critiques and a recorded dispute sitting over the
    second's BLOCKER and MAJOR findings, whose findings file the filing step
    writes."""
    lane, text = second_critique(tmp_path, second)
    ids = blocking(text)
    positions = "".join("{}: Contested.\n".format(fid) for fid in ids)
    rb.write_dispute_findings(lane, WI, positions, FINDINGS)
    write(lane, VERDICT, "Judged.\n\n{}\n".format(ruling))
    write(
        lane,
        VERDICT + ".requested",
        "brief = dispute\nkinds = {}\noutcome = {}\n".format(";".join(ids), outcome),
    )
    commit(lane, "the dispute sitting")
    return lane, text


def blocking(text):
    return [k for k, v in rb.critique_findings(text).items() if "[MINOR]" not in v]


def test_at_the_cap_an_accepted_dismissal_of_every_blocking_finding_passes(tmp_path):
    lane, _sha = cap(tmp_path)
    assert rb.write_pass(lane, WI, VERDICT).is_file()
    assert staged(lane) == []
    commit(lane, "pass")
    write(lane, "src/app.py", "x = 1\n")
    assert staged(lane) == []
    git(lane, "reset", "-q")
    sha = git(lane, "rev-parse", "HEAD")
    later = write(tmp_path, "scratch/v3.md", critique_text(sha))
    assert file_cli(lane, later, sha) == 2  # no third critique


@pytest.mark.parametrize(
    "ruling, outcome",
    [
        ("RULING: F1 FIX the plan lacks the test", "accepted"),
        ("RULING: F1 ESCALATE owner call", "accepted"),
        ("RULING: F1 DISMISS refuted no", "failed"),
    ],
)
def test_at_the_cap_anything_but_an_accepted_dismissal_is_refused(
    tmp_path, ruling, outcome
):
    lane, _sha = cap(tmp_path, ruling, outcome)
    with pytest.raises(rb.BriefError):
        rb.write_pass(lane, WI, VERDICT)
    with pytest.raises(rb.BriefError, match="dispute"):
        rb.write_pass(lane, WI)
    assert not (lane / pp.record_path(WI)).exists()


def test_at_the_cap_a_successor_ruling_never_passes(tmp_path):
    """WI-911: SUCCESSOR resolves a finding on the rework gate only. At the
    plan cap only an accepted dismissal writes a pass record (SR-154), so a
    verdict ruling the blocking finding SUCCESSOR writes none."""
    lane, _sha = cap(tmp_path, "RULING: F1 SUCCESSOR file a row for the test")
    with pytest.raises(rb.BriefError) as refused:
        rb.write_pass(lane, WI, VERDICT)
    said = str(refused.value)
    assert "rules it SUCCESSOR" in said and "only a DISMISS" in said, said
    assert "SUCCESSOR resolves" not in said and "or a SUCCESSOR" not in said, said
    assert not (lane / pp.record_path(WI)).exists()


def test_at_the_cap_a_major_after_a_minor_is_disputed_under_its_own_number(tmp_path):
    # Opus REVIEW-B F1 (round 1): a finding's number is its position among
    # ALL the critique's findings, so a MAJOR after a MINOR is F2, and the
    # findings file the filing step writes says so.
    ruling = "RULING: F2 DISMISS refuted the plan has the test"
    lane, _sha = cap(tmp_path, ruling, second=(MINOR, MAJOR))
    found, _why = kdispute.read_findings((lane / FINDINGS).read_text("utf-8"), "f")
    assert [f["id"] for f in found["findings"]] == ["F2"]
    assert rb.write_pass(lane, WI, VERDICT).is_file()


def test_at_the_cap_two_blocking_findings_with_one_dismissed_are_refused(tmp_path):
    ruling = "RULING: F1 DISMISS refuted yes\nRULING: F2 FIX the plan needs it"
    lane, _sha = cap(tmp_path, ruling, second=(MAJOR, MAJOR2))
    with pytest.raises(rb.BriefError, match="F2: the dispute verdict rules it FIX"):
        rb.write_pass(lane, WI, VERDICT)
    assert not (lane / pp.record_path(WI)).exists()


@pytest.mark.parametrize("positions", ["F1: Contested.\n", "F2: x\nF3: y\n", ""])
def test_the_dispute_findings_file_refuses_ids_other_than_the_blocking_ones(
    tmp_path, positions
):
    lane, _text = second_critique(tmp_path, (MINOR, MAJOR))
    argv = ["plan-file", "--root", str(lane), "--wi", WI]
    argv += ["--dispute-findings", FINDINGS]
    argv += ["--positions", str(write(tmp_path, "scratch/pos.md", positions))]
    assert rb.main(argv) == 2
    assert clean(lane) == ""
    write(tmp_path, "scratch/pos.md", "F2: Contested.\n")
    assert rb.main(argv) == 0
    assert git(lane, "status", "--porcelain", "-uall") == "?? " + FINDINGS


def test_at_the_cap_an_uncommitted_dispute_verdict_is_refused(tmp_path):
    lane, _sha = cap(tmp_path)
    (lane / VERDICT).write_text(
        "Judged.\n\nRULING: F1 DISMISS refuted later\n", encoding="utf-8"
    )
    with pytest.raises(rb.BriefError, match="HEAD does not hold"):
        rb.write_pass(lane, WI, VERDICT)


# --- the plan critique's brief --------------------------------------------------------


def test_the_plan_critique_renders_over_the_committed_plan_and_its_coverage(tmp_path):
    lane, sha = planned(tmp_path)
    brief, verdict = rb.render_plan_critique(lane, WI, RUBRIC, sha, str(tmp_path / "s"))
    assert verdict.endswith("WI-950-plan-critique-1.md")
    assert "scope-critique" not in verdict
    assert "`Reviewed: {}`".format(sha) in brief
    assert "### Coverage report" in brief and "covers: D1 D2 (2/2)" in brief
    assert "convergence stance" not in brief
    assert "Plan decomposition" in brief


# The reachability gate every severity site states in one wording, after its
# own BLOCKER-or-MAJOR clause; its home is PROCESS.md §6 "Review threat model".
REACH_GATE = (
    "a fail-open, data-loss or security path counts only when a supported "
    "workflow or the kit's own routes reach it; a rare or contrived path is "
    'MINOR at most, or dismissed under PROCESS.md §6 "Review threat model".'
)


def test_the_plan_critique_brief_ties_severity_to_reachability(tmp_path):
    # WI-911 (review-churn item 4): the live rubric's verdict section carries
    # the severity rule into the plan critique's brief by render, so no
    # by-hand addendum is needed once the trial recipe retired.
    lane, sha = planned(tmp_path)
    brief, _verdict = rb.render_plan_critique(
        lane, WI, RUBRIC, sha, str(tmp_path / "s")
    )
    flat = " ".join(brief.split())
    assert (
        "a BLOCKER or MAJOR states a defect in the plan that would reasonably "
        "cost a build or review round in normal use, and " + REACH_GATE
    ) in flat


def test_the_second_plan_critique_is_in_convergence_and_never_sees_the_first(tmp_path):
    lane, sha = planned(tmp_path)
    first = critique_text(sha, "CHANGES-REQUESTED", [MAJOR])
    rb.file_plan_critique(lane, WI, first, sha)
    commit(lane, "critique 1")
    revised = PLAN.replace("| D2 | intra-module", "| D2; F1 | intra-module")
    write(lane, pp.plan_path(WI), revised)
    sha2 = commit(lane, "the one revision")
    brief, verdict = rb.render_plan_critique(
        lane, WI, RUBRIC, sha2, str(tmp_path / "s")
    )
    assert verdict.endswith("WI-950-plan-critique-2.md")
    assert "convergence stance" in brief
    assert "P2 has no test" not in brief
    # Reachability gates the convergence classes too.
    assert (
        "A new finding is BLOCKER or MAJOR only if it is fail-open, data loss or "
        "a Done-when gap, and a supported workflow or the kit's own routes reach "
        "it; anything else is MINOR."
    ) in " ".join(brief.split())


def test_the_second_critique_refuses_a_revision_that_misses_a_first_finding(tmp_path):
    # Opus REVIEW-B F5 (round 1): the revision is gated against the first
    # critique's findings before the second critic's run is spent on it.
    lane, sha = planned(tmp_path)
    first = critique_text(sha, "CHANGES-REQUESTED", [MAJOR])
    rb.file_plan_critique(lane, WI, first, sha)
    commit(lane, "critique 1")
    write(lane, pp.plan_path(WI), PLAN.replace("Release it", "Release it now"))
    sha2 = commit(lane, "a revision that answers nothing")
    out = tmp_path / "out" / "brief.md"
    argv = ["critique", "--plan", "--root", str(lane), "--wi", WI, "--sha", sha2]
    argv += ["--rubric", RUBRIC, "--scratch", str(tmp_path / "s"), "--out", str(out)]
    assert rb.main(argv) == 2
    assert not out.exists()
    with pytest.raises(rb.BriefError, match="first critique's findings"):
        rb.render_plan_critique(lane, WI, RUBRIC, sha2, str(tmp_path / "s"))


@pytest.mark.parametrize("missing", ["rubric", "plan", "spec", "beyond"])
def test_the_plan_critique_refuses_a_missing_input_and_writes_nothing(
    tmp_path, missing
):
    lane, sha = planned(tmp_path)
    out = tmp_path / "out" / "brief.md"
    argv = ["critique", "--plan", "--root", str(lane), "--wi", WI, "--sha", sha]
    argv += ["--rubric", "docs/rubrics/none.md" if missing == "rubric" else RUBRIC]
    argv += ["--scratch", str(tmp_path / "s"), "--out", str(out)]
    if missing == "plan":
        git(lane, "rm", "-q", pp.plan_path(WI))
        argv[argv.index(sha)] = commit(lane, "no plan")
    if missing == "spec":
        argv[argv.index(WI)] = "WI-999"
    if missing == "beyond":
        write(lane, pp.plan_path(WI), PLAN.replace("DELTA: none", "DELTA: beyond"))
        argv[argv.index(sha)] = commit(lane, "beyond")
    assert rb.main(argv) == 2
    assert not out.exists()
    assert BRANCH in git(lane, "branch", "--show-current")
