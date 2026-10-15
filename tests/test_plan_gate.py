"""The plan gate on a real lane (WI-913): a row whose claim copy declares
`planmode = "single"` builds only after a pass record binds its plan.

Each case builds a trunk (`main`, the primary checkout) holding the claim and
a linked lane worktree on `wi-950`, and drives the one predicate where it is
asked: the pre-commit hook's `plan-gate` step (`plan_gate.staged_lines`, once
through `check.py --run-steps`), a squash landing on trunk, and the merge
slot's walk of each lane commit (`plan_gate.landing_refusal`). The plan, its
critique and the pass record are written through the filing step
(`review_brief.py plan-file`), in the two-commit order the gate requires.
They spawn git, so this module is in `tests/conftest.py`'s `SLOW_MODULES`;
the in-process pin is `test_plan_pass.py`.
"""

import shutil
import subprocess

import pytest
from conftest import SCRIPTS, load_script, pin_autocrlf, run_py

gate = load_script("plan_gate")
rb = load_script("review_brief")
integrate = load_script("integrate")
from kitlib import plan_pass as pp  # noqa: E402  (scripts/ put on the path above)

WI = "WI-950"
BRANCH = "wi-950"
SPEC_REL = "docs/work/active/wi-950/WI-950-plan-first.md"
SPEC = """+++
id = "WI-950"
title = "A row that plans first"
sr_refs = ["SR-001"]
planmode = "{mode}"
+++

## Done-when

- The gate holds the build.
- The record releases it.
"""
PLAN = """# Plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Hold the build | D1; SR-001 | intra-module | |
| P2 | Release it | D2 | intra-module | P1 |

DELTA: none
"""


def git(root, *args):
    proc = subprocess.run(
        [shutil.which("git"), "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip()


def write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def commit(root, msg="c"):
    git(root, "add", "-A")
    git(root, "commit", "-q", "--no-verify", "-m", msg)
    return git(root, "rev-parse", "HEAD")


def staged(root):
    git(root, "add", "-A")
    return gate.staged_lines(root)


def make_trunk(tmp_path, mode="single", extra=()):
    trunk = tmp_path / "trunk"
    trunk.mkdir(parents=True)
    git(trunk, "init", "-q", "-b", "main")
    pin_autocrlf(trunk)
    for key, value in (("user.email", "t@example.com"), ("user.name", "t")):
        git(trunk, "config", key, value)
    git(trunk, "config", "commit.gpgsign", "false")
    write(trunk, "README.md", "r\n")
    write(trunk, SPEC_REL, SPEC.format(mode=mode))
    for rel, text in extra:
        write(trunk, rel, text)
    commit(trunk, "claim: WI-950 -> active/wi-950")
    return trunk


def make_lane(tmp_path, mode="single", extra=()):
    """`(trunk, lane)`: trunk holds the claim; the lane is its linked worktree."""
    trunk = make_trunk(tmp_path, mode, extra)
    lane = tmp_path / "lane"
    git(trunk, "worktree", "add", "-q", "-b", BRANCH, str(lane))
    return trunk, lane


def critique_text(sha, verdict="APPROVE", findings=()):
    lines = ["Reviewed: " + sha, "", "Verified: the plan.", ""]
    lines += list(findings)
    lines.append("VERDICT: {} findings={}".format(verdict, len(findings)))
    return "\n".join(lines) + "\n"


def plan_and_pass(lane, plan=PLAN, verdict="APPROVE", findings=()):
    """The plan step, as the recipe runs it: commit the plan, file its
    critique and commit it alone, then write the pass record and commit it
    alone. Returns the plan commit."""
    write(lane, pp.plan_path(WI), plan)
    sha = commit(lane, "plan")
    rb.file_plan_critique(lane, WI, critique_text(sha, verdict, findings), sha)
    assert staged(lane) == []
    commit(lane, "critique")
    rb.write_pass(lane, WI)
    assert staged(lane) == []
    commit(lane, "pass")
    return sha


def build(lane, name="src/app.py"):
    write(lane, name, "x = 1\n")
    return staged(lane)


def unbuild(lane):
    """Drop the staged build output a held commit left behind."""
    git(lane, "reset", "-q")
    shutil.rmtree(lane / "src", ignore_errors=True)


# --- the build is held until a pass record binds the plan ---------------------


def test_a_build_without_a_pass_record_is_refused_at_the_hook_and_the_landing(
    tmp_path,
):
    trunk, lane = make_lane(tmp_path)
    (line,) = build(lane)
    assert WI in line and "src/app.py" in line and "no plan at" in line
    proc = run_py([SCRIPTS / "check.py", "--run-steps", "plan-gate"], lane)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "FAIL  plan-gate" in proc.stdout
    commit(lane, "build")
    refusal = gate.landing_refusal(trunk, git(trunk, "rev-parse", "HEAD"), BRANCH)
    assert refusal and "nothing was merged" in refusal and WI in refusal
    git(trunk, "merge", "--squash", BRANCH)
    assert any("src/app.py" in ln for ln in gate.staged_lines(trunk))


def test_a_build_after_its_pass_record_is_not_refused_anywhere(tmp_path):
    trunk, lane = make_lane(tmp_path)
    plan_and_pass(lane)
    assert build(lane) == []
    commit(lane, "build")
    assert gate.landing_refusal(trunk, git(trunk, "rev-parse", "HEAD"), BRANCH) is None
    git(trunk, "merge", "--squash", BRANCH)
    assert gate.staged_lines(trunk) == []


_EARLIER_RUNGS = (
    "_close_record_refusal",
    "_done_when_refusal",
    "_minted_id_refusal",
    "_approval_act_refusal",
    "_held_status_refusal",
    "_loop_trailer_refusal",
    "_ruling_sync_refusal",
    "_text_then_act_refusal",
)


def test_the_merge_slot_asks_the_gate_of_each_lane_commit(tmp_path, monkeypatch):
    # Fable REVIEW-B F3 (round 1): drive the slot's ladder itself, its other
    # rungs passing, rather than reading its source.
    trunk, lane = make_lane(tmp_path)
    for name in _EARLIER_RUNGS:
        monkeypatch.setattr(integrate, name, lambda *_a, **_k: None)
    monkeypatch.setattr(integrate, "branch_outcomes", lambda *_a: ({}, []))
    monkeypatch.setattr(integrate, "_review_scope_refusal", lambda *_a: "NEXT RUNG")
    build(lane)
    commit(lane, "build")
    _outcomes, refusal = integrate._merge_refusal(trunk, BRANCH, [WI])
    assert refusal and WI in refusal and "nothing was merged" in refusal
    assert "src/app.py" in refusal
    git(lane, "reset", "-q", "--hard", "HEAD~1")
    plan_and_pass(lane)
    build(lane)
    commit(lane, "build")
    assert integrate._merge_refusal(trunk, BRANCH, [WI])[1] == "NEXT RUNG"


@pytest.mark.parametrize("raw", ["false", "0", "[]", "{}"])
def test_a_non_string_planmode_holds_at_the_hook_and_the_landing(tmp_path, raw):
    # Sol REVIEW-A F1 (round 1): these failed open as the ungated empty value.
    trunk = make_trunk(tmp_path)
    spec = (trunk / SPEC_REL).read_text(encoding="utf-8")
    write(trunk, SPEC_REL, spec.replace('planmode = "single"', "planmode = " + raw))
    commit(trunk, "claim with a raw planmode")
    lane = tmp_path / "lane"
    git(trunk, "worktree", "add", "-q", "-b", BRANCH, str(lane))
    (line,) = build(lane)
    assert WI in line and "not a string" in line
    commit(lane, "build")
    refusal = gate.landing_refusal(trunk, git(trunk, "rev-parse", "HEAD"), BRANCH)
    assert refusal and "not a string" in refusal


@pytest.mark.parametrize("mode, held", [("single", True), ("dual", False)])
def test_a_squash_no_local_branch_contains_is_held_by_name(tmp_path, mode, held):
    # Fable REVIEW-B F1 (round 1): a squashed tip no local branch contains
    # (its branch deleted) was judged by nothing at the hook.
    trunk, lane = make_lane(tmp_path, mode)
    build(lane)
    tip = commit(lane, "build")
    git(lane, "checkout", "-q", "--detach")
    git(trunk, "branch", "-q", "-D", BRANCH)
    git(trunk, "merge", "--squash", tip)
    lines = gate.staged_lines(trunk)
    assert bool(lines) is held
    if held:
        assert tip[:10] in lines[0] and "no local branch" in lines[0]


# --- what the record binds ---------------------------------------------------------


def test_a_plan_edited_after_its_record_is_refused_until_a_new_record_binds_it(
    tmp_path,
):
    _trunk, lane = make_lane(tmp_path)
    plan_and_pass(lane)
    edited = PLAN.replace("Release it", "Release it later")
    write(lane, pp.plan_path(WI), edited)
    assert staged(lane) == []  # the plan home itself is never held
    commit(lane, "edit the plan")
    (line,) = build(lane)
    assert "binds another plan" in line and "new critique" in line
    unbuild(lane)
    git(lane, "rm", "-q", pp.record_path(WI))
    commit(lane, "unbind")
    sha = git(lane, "rev-parse", "HEAD")
    rb.file_plan_critique(lane, WI, critique_text(sha), sha)
    commit(lane, "critique 2")
    rb.write_pass(lane, WI)
    commit(lane, "pass 2")
    assert build(lane) == []


def test_a_done_when_edit_unbinds_and_a_tick_does_not(tmp_path):
    _trunk, lane = make_lane(tmp_path)
    plan_and_pass(lane)
    spec = (lane / SPEC_REL).read_text(encoding="utf-8")
    write(lane, SPEC_REL, spec.replace("- The gate holds", "- [x] The gate holds"))
    commit(lane, "tick")
    assert build(lane) == []
    unbuild(lane)
    write(lane, SPEC_REL, spec.replace("The record releases it.", "Nothing more."))
    commit(lane, "reword")
    (line,) = build(lane, "src/b.py")
    assert "binds another done-when" in line


def test_absent_unreadable_and_malformed_records_hold(tmp_path, monkeypatch):
    _trunk, lane = make_lane(tmp_path)
    write(lane, pp.plan_path(WI), PLAN)
    commit(lane, "plan")
    (absent,) = build(lane)
    assert "no pass record" in absent
    unbuild(lane)
    write(lane, pp.record_path(WI), 'wi = "WI-950"\n')
    commit(lane, "a partial record")
    (malformed,) = build(lane, "src/b.py")
    assert "malformed" in malformed
    real = pp.blob
    rec = pp.record_path(WI)

    def unreadable(root, rev, rel):
        return (
            (None, rel + " cannot be read at x") if rel == rec else real(root, rev, rel)
        )

    monkeypatch.setattr(pp, "blob", unreadable)
    (line,) = gate.staged_lines(lane)
    assert "cannot be read" in line


def test_a_record_naming_another_row_or_digest_holds(tmp_path):
    _trunk, lane = make_lane(tmp_path)
    plan_and_pass(lane)
    record = (lane / pp.record_path(WI)).read_text(encoding="utf-8")
    write(lane, pp.record_path(WI), record.replace("WI-950", "WI-951"))
    commit(lane, "another row")
    (line,) = build(lane)
    assert "names another row" in line
    unbuild(lane)
    fields, _why = pp.parse(record)
    other = pp.render({**fields, "plan": "sha256:" + "0" * 64})
    write(lane, pp.record_path(WI), other)
    commit(lane, "another digest")
    (line,) = build(lane, "src/b.py")
    assert "binds another plan" in line


# --- the pass-record commit is checked against its parent -------------------------


def test_a_pass_record_committed_with_its_critique_is_refused_and_the_two_commit_order_passes(
    tmp_path,
):
    _trunk, lane = make_lane(tmp_path)
    write(lane, pp.plan_path(WI), PLAN)
    sha = commit(lane, "plan")
    rb.file_plan_critique(lane, WI, critique_text(sha), sha)
    commit(lane, "critique")
    rb.write_pass(lane, WI)
    record = (lane / pp.record_path(WI)).read_bytes()
    (lane / pp.record_path(WI)).unlink()
    git(lane, "reset", "-q", "--hard", sha)  # back before the critique's commit
    rb.file_plan_critique(lane, WI, critique_text(sha), sha)
    (lane / pp.record_path(WI)).write_bytes(record)
    lines = staged(lane)
    assert any("is not in" in ln and "critique" in ln for ln in lines), lines
    git(lane, "reset", "-q")
    (lane / pp.record_path(WI)).unlink()
    assert staged(lane) == []
    commit(lane, "critique alone")
    (lane / pp.record_path(WI)).write_bytes(record)
    assert staged(lane) == []


def test_a_pass_record_whose_digests_its_parent_does_not_support_is_refused(tmp_path):
    _trunk, lane = make_lane(tmp_path)
    write(lane, pp.plan_path(WI), PLAN)
    sha = commit(lane, "plan")
    rb.file_plan_critique(lane, WI, critique_text(sha), sha)
    commit(lane, "critique")
    fields = rb.pass_fields(lane, WI)
    write(lane, pp.record_path(WI), pp.render({**fields, "plan": "sha256:" + "1" * 64}))
    (line, *_rest) = staged(lane)
    assert "plan digest" in line
    write(
        lane,
        pp.record_path(WI),
        pp.render({**fields, "done_when": "sha256:" + "2" * 16}),
    )
    assert any("Done-when digest" in ln for ln in staged(lane))


def test_a_pass_record_whose_critique_reviewed_another_plan_is_refused(tmp_path):
    _trunk, lane = make_lane(tmp_path)
    write(lane, pp.plan_path(WI), PLAN)
    old = commit(lane, "plan")
    rb.file_plan_critique(lane, WI, critique_text(old), old)
    write(lane, pp.plan_path(WI), PLAN.replace("Release it", "Release it now"))
    commit(lane, "critique, and the plan changed after it")
    plan, delta, _w = pp.plan_digest(lane, "HEAD", WI)
    with pytest.raises(rb.BriefError, match="reviewed other plan bytes"):
        rb.write_pass(lane, WI)
    data = (lane / pp.critique_path(WI, 1)).read_bytes()
    claimed = (lane / SPEC_REL).read_text(encoding="utf-8")
    done, _w = pp.done_when_digest(lane, "HEAD", BRANCH, WI, claimed)
    forged = dict.fromkeys(pp.FIELDS, "")
    forged.update(wi=WI, plan=plan, done_when=done, delta=delta, reviewed=old)
    forged.update(
        critique=pp.critique_path(WI, 1), critique_digest=pp.bytes_digest(data)
    )
    write(lane, pp.record_path(WI), pp.render(forged))
    assert any("reviewed other plan bytes" in ln for ln in staged(lane))


def test_a_pass_record_whose_critique_reviewed_another_done_when_is_refused(tmp_path):
    # Opus REVIEW-B F2 (round 2): the Done-when-digest arm, at the pass form
    # and at the pass-record commit, beside the plan-bytes arm above.
    _trunk, lane = make_lane(tmp_path)
    write(lane, pp.plan_path(WI), PLAN)
    old = commit(lane, "plan")
    rb.file_plan_critique(lane, WI, critique_text(old), old)
    spec = (lane / SPEC_REL).read_text(encoding="utf-8")
    write(lane, SPEC_REL, spec.replace("The record releases it.", "Nothing more."))
    commit(lane, "critique, and the Done-when changed after it")
    with pytest.raises(rb.BriefError, match="another Done-when"):
        rb.write_pass(lane, WI)
    plan, delta, _w = pp.plan_digest(lane, "HEAD", WI)
    data = (lane / pp.critique_path(WI, 1)).read_bytes()
    claimed = (lane / SPEC_REL).read_text(encoding="utf-8")
    done, _w = pp.done_when_digest(lane, "HEAD", BRANCH, WI, claimed)
    forged = dict.fromkeys(pp.FIELDS, "")
    forged.update(wi=WI, plan=plan, done_when=done, delta=delta, reviewed=old)
    forged.update(
        critique=pp.critique_path(WI, 1), critique_digest=pp.bytes_digest(data)
    )
    write(lane, pp.record_path(WI), pp.render(forged))
    assert any("another Done-when" in ln for ln in staged(lane))


# --- the shipped hook selects the step ---------------------------------------------


def hook_floor():
    """The step list the shipped pre-commit hook hands `check.py
    --run-steps`, read off the hook as it invokes it."""
    hook = (SCRIPTS.parent / "hooks" / "pre-commit").read_text(encoding="utf-8")
    line = next(
        ln for ln in hook.splitlines() if ln.startswith('"$PY"') and "--run-steps" in ln
    )
    return line.split("--run-steps", 1)[1].split()[0]


def test_the_shipped_hooks_floor_refuses_an_unplanned_build(tmp_path):
    # Sol REVIEW-A F1 (round 2): the step was registered but the shipped
    # hook never selected it, so an unplanned build passed the hook.
    _trunk, lane = make_lane(tmp_path)
    build(lane)
    proc = run_py([SCRIPTS / "check.py", "--run-steps", hook_floor()], lane)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "FAIL  plan-gate" in proc.stdout and "src/app.py" in proc.stdout


# --- the record homes, a close, a rebase and a merge ------------------------------


@pytest.mark.parametrize(
    "rel",
    [
        "docs/plans/WI-950/plan.md",
        "docs/reviews/wi-950/001-ADJUDICATE-abc1234.md",
        "docs/decisions/wi-950.toml",
        "docs/iteration/001-x.log",
        SPEC_REL,
        # Opus REVIEW-B F1 (round 2): a work branch's log fragment.
        pytest.param("docs/log.d/WI-950-plan-first.md", id="log-fragment"),
    ],
)
def test_each_record_home_passes_before_any_record(tmp_path, rel):
    _trunk, lane = make_lane(tmp_path)
    write(lane, rel, "a record\n")
    assert staged(lane) == []


def test_a_close_of_the_row_passes_before_any_record(tmp_path):
    spec_move = load_script("spec_move")
    station_report = "docs/handbacks/WI-950-wi-950.md"
    linker = (
        "docs/notes.md",
        "See [the row](work/active/wi-950/WI-950-plan-first.md).\n",
    )
    _trunk, lane = make_lane(tmp_path, extra=(linker,))
    dest = "docs/work/partial/WI-950-plan-first.md"
    _touched, refusal = spec_move.move_spec(lane, SPEC_REL, dest)
    assert refusal is None
    write(lane, station_report, "the report\n")
    assert "partial/" in (lane / "docs" / "notes.md").read_text(encoding="utf-8")
    assert staged(lane) == []
    write(lane, "docs/notes.md", "a different edit\n")
    assert any("docs/notes.md" in ln for ln in staged(lane))


def test_a_refresh_merge_of_a_partial_closed_lane_passes(tmp_path):
    # Opus REVIEW-B F1 (round 2): the station refresh merges trunk in,
    # compiles the log fragments into docs/log.md and regenerates the views
    # trunk_step lists; those are the merge's own changes, and a lane closed
    # partial before any record must still land through it.
    spec_move = load_script("spec_move")
    view = ("PROJECT_STATE.html", "<html>old</html>\n")
    trunk, lane = make_lane(tmp_path, extra=(view, ("docs/log.md", "# Log\n")))
    write(lane, "docs/log.d/WI-950-plan-first.md", "the lane's evidence\n")
    dest = "docs/work/partial/WI-950-plan-first.md"
    assert spec_move.move_spec(lane, SPEC_REL, dest)[1] is None
    write(lane, "docs/handbacks/WI-950-wi-950.md", "the report\n")
    assert staged(lane) == []
    commit(lane, "close partial")
    write(trunk, "docs/log.d/WI-951-other.md", "another lane\n")
    commit(trunk, "trunk moves on")
    git(lane, "merge", "-q", "--no-commit", "--no-ff", "main")
    for rel in ("docs/log.d/WI-950-plan-first.md", "docs/log.d/WI-951-other.md"):
        (lane / rel).unlink()
    write(lane, "docs/log.md", "# Log\n\nthe lane's evidence\nanother lane\n")
    write(lane, "PROJECT_STATE.html", "<html>regenerated</html>\n")
    assert staged(lane) == []
    commit(lane, "refresh")
    assert gate.landing_refusal(trunk, git(trunk, "rev-parse", "HEAD"), BRANCH) is None
    write(lane, "PROJECT_STATE.html", "<html>by hand</html>\n")
    (line,) = staged(lane)  # outside a merge, a generated view is build output
    assert "PROJECT_STATE.html" in line


def test_a_rebased_lanes_record_still_binds(tmp_path):
    trunk, lane = make_lane(tmp_path)
    plan_and_pass(lane)
    write(trunk, "other.txt", "trunk moved\n")
    commit(trunk, "trunk moves on")
    git(lane, "rebase", "-q", "main")
    assert build(lane) == []
    commit(lane, "build")
    assert gate.landing_refusal(trunk, git(trunk, "rev-parse", "HEAD"), BRANCH) is None


def test_a_merge_is_judged_by_what_neither_parent_carried(tmp_path):
    trunk, lane = make_lane(tmp_path)
    write(lane, pp.plan_path(WI), PLAN)
    commit(lane, "plan")
    write(trunk, "src/trunk.py", "y = 2\n")
    commit(trunk, "trunk builds something")
    git(lane, "merge", "-q", "--no-commit", "--no-ff", "main")
    assert gate.staged_lines(lane) == []  # trunk's file is trunk's, not the lane's
    write(lane, "src/resolution.py", "z = 3\n")
    (line,) = staged(lane)
    assert "src/resolution.py" in line and "src/trunk.py" not in line


# --- whose claim copy, and which planmode -----------------------------------------


def test_a_lane_editing_its_own_planmode_is_still_held(tmp_path):
    _trunk, lane = make_lane(tmp_path)
    spec = (lane / SPEC_REL).read_text(encoding="utf-8")
    write(lane, SPEC_REL, spec.replace('planmode = "single"', 'planmode = "none"'))
    commit(lane, "unmark")
    (line,) = build(lane)
    assert WI in line


def test_another_lanes_single_claim_copy_does_not_hold_this_lane(tmp_path):
    other = (
        "docs/work/active/wi-951/WI-951-other.md",
        SPEC.format(mode="single").replace("WI-950", "WI-951"),
    )
    _trunk, lane = make_lane(tmp_path, mode="none", extra=(other,))
    assert build(lane) == []


@pytest.mark.parametrize(
    "mode, held",
    [
        ("absent", False),
        ("", False),
        ("none", False),
        ("dual", False),
        (" Single ", True),
        ("weird", True),
    ],
)
def test_the_planmode_set_is_closed(tmp_path, mode, held):
    trunk = make_trunk(tmp_path, mode)
    if mode == "absent":
        spec = (trunk / SPEC_REL).read_text(encoding="utf-8")
        write(trunk, SPEC_REL, spec.replace('planmode = "absent"\n', ""))
        commit(trunk, "no planmode at all")
    rows, claimed, holds = pp.gate_rows(trunk, "HEAD", BRANCH)
    assert claimed == [WI]
    assert bool(rows or holds) is held
    if mode == "weird":
        assert "'weird'" in holds[0]


def test_trunk_commits_and_a_lane_with_no_single_row_are_not_judged(tmp_path):
    trunk, _lane = make_lane(tmp_path / "single")
    assert build(trunk) == []
    _trunk, lane = make_lane(tmp_path / "dual", mode="dual")
    assert build(lane) == []
