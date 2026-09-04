"""dispatch.py — the dispatcher loop (WI-374; renamed from drive.py at WI-381).

The dispatch loop is COMPOSITION: schedule.py's frontier picks, integrate.py
claims and merges, agent_loop.py's worker role builds (launched by lane.py).
What this module pins is the loop's own contract — the joints, not the parts
(each part's own suite already pins it):

  * an unwired agent command refuses BEFORE anything is claimed;
  * an empty frontier drains the queue and exits 0 — success, not an error;
  * a refusing claim rung stops the run loudly (never skipped);
  * the tracked pause appearing MID-RUN stops the next cycle (exit 8);
  * a worker that reports DONE without finishing its branch trips the drive
    loop's own stall guard (the trunk-unmoved counter);
  * a worker that could not finish HANDS BACK (WI-387, §A3) — NEEDS-HUMAN no
    longer stops the run, the WI returns to trunk blocked, and the loop drives
    on to the drained banner; a red handback is reverted to a bar-inert
    artefact and merges anyway; a CRASHED worker is not a handback and keeps
    the parked-resume path;
  * end-to-end on a REAL scaffold: claim -> injected worker close -> the REAL
    §A2 refresh bar -> merge -> drained banner; and the same flow with a
    breaking change stops on the RED bar with the branch still parked;
  * the SPECULATIVE half of the station protocol (WI-386): `_drain` refreshes
    every finished branch BEFORE it takes the merge slot, so the 11-minute bar
    never holds the exclusive turn to advance trunk. That one call is the whole
    speculation — deleting it restricts the design to pessimistic, which the
    integrator's own suite covers from the other side.

The worker seam is injected in every test (`run(root, args, worker=...)`) —
the real subprocess launch of agent_loop.py --wi is agent_loop's own tested
surface — but integrate.py and the bar are REAL: a stubbed bar here would be
exactly the vacuous green the integrator exists to make impossible. Git
fixtures are real repositories for the same reason as tests/test_integrate.py
(the queue derives everything from history), and the helper shapes are copied
from that module per this suite's no-cross-test-import idiom.
"""

import argparse
import os
import subprocess

from conftest import (
    SCRIPTS,
    disable_blackout,
    env_gate_skipif,
    load_script,
    make_minimal_project,
    pin_autocrlf,
    record_ids,
    run_py,
    set_process_key,
    skip_without_env_gates,
)

pytestmark = env_gate_skipif("git")

drv = load_script("dispatch")
# The attestation constant has ONE home; a literal here would be a second one
# that could drift silently past every test in this file.
integ = drv.integrate

T_BASE = 1_000_000
T_CODE = 1_000_100
T_LATER = 1_000_200


def _git(root, *args, env=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message, when=None):
    env = dict(os.environ)
    if when is not None:
        stamp = "@{} +0000".format(when)
        env["GIT_AUTHOR_DATE"] = stamp
        env["GIT_COMMITTER_DATE"] = stamp
    _git(root, "add", "-A", env=env)
    _git(root, "commit", "-qm", message, env=env)


def git_repo(root, branch="main"):
    skip_without_env_gates("git")
    _git(root, "init", "-q")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/" + branch)
    (root / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    # out/ holds integrate.py's lock file, which persists between drains; an
    # unignored one reads as dirt at the NEXT cycle's clean-trunk check (the
    # same stock-scaffold finding tests/test_integrate.py records).
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    write_watermark(root, WI=401)
    _commit(root, "seed", when=T_BASE)
    return root


def write_watermark(root, **marks):
    """Give a bare fixture repo the `docs/id-watermark` every real repo carries.

    `trace.read_watermark` RAISES on an absent file rather than reading it as
    "no id is taken" — and the intake mint reads the mark to pick the next id,
    so a repo without one cannot mint at all. Seeded here (before any claim) so
    the file is repo furniture rather than something a later trunk commit
    introduces."""
    body = "".join(
        "{} = {}\n".format(space, marks.get(space, 0))
        for space in "ASSET CMP DP IF LLR MOD OI PART PB REPO SN SR TC WI".split()
    )
    path = root / "docs" / "id-watermark"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8", newline="\n")
    return path


def spec_text(
    wid, safety="ordinary", specref=None, deliverable="A widget, shipped.", bar=None
):
    lines = [
        'id = "{}"'.format(wid),
        'title = "Widget"',
        'workstream = "ws"',
        'sr_refs = ["SR-001"]',
        "needs = []",
        'safety_class = "{}"'.format(safety),
        "order = 0",
    ]
    if bar:
        lines.append('bar = "{}"'.format(bar))
    if specref:
        lines.append('specref = "{}"'.format(specref))
    text = "+++\n" + "".join(ln + "\n" for ln in lines) + "+++\n"
    if deliverable:
        text += "\n## Deliverable\n\n" + deliverable + "\n"
    return text


def write_spec(root, where, wid, slug="widget", **kw):
    path = root / "docs" / "work" / where / "{}-{}.md".format(wid, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(spec_text(wid, **kw), encoding="utf-8", newline="\n")
    return path


def drive_args(**kw):
    """The argparse surface drive.run reads, with per-test overrides."""
    ns = argparse.Namespace(
        agent_cmd="stub-agent",
        session_timeout=0,
        no_session_echo=False,
        live_status=False,
        max_iterations=10,
        stall_limit=3,
        lanes=None,
        model="",
        model_map="",
        cmd_map="",
        prompt_map="",
        tier_map="",
        prefer_map="",
        wait_on_limit=0,
        limit_retry_fallback=3600,
    )
    for k, v in kw.items():
        setattr(ns, k, v)
    return ns


def parked_repo(tmp_path, wid="WI-401", branch="wi-401"):
    """An interrupted run's state: the trunk holds active/<branch>/<spec> and
    the branch exists with that same tree (unfinished — the spec never moved
    to complete/), which is exactly what _parked_branches must resume."""
    root = git_repo(tmp_path)
    write_spec(root, "active/" + branch, wid, specref="seed.txt")
    _commit(root, "claim: {} -> active/{}".format(wid, branch), when=T_CODE)
    _git(root, "branch", branch)
    return root


class Recorder:
    """A worker stand-in that records calls and plays scripted exit codes."""

    def __init__(self, outcomes=(0,), effect=None):
        self.calls = []
        self.outcomes = list(outcomes)
        self.effect = effect

    def __call__(self, root, branch, wi_ids, args):
        self.calls.append((branch, tuple(wi_ids)))
        if self.effect is not None:
            self.effect(root, branch, wi_ids)
        return self.outcomes.pop(0) if self.outcomes else 0


# --- preflight and the empty frontier -----------------------------------------


def test_drive_refuses_an_unwired_agent_command_before_claiming(
    tmp_path, capfd, monkeypatch
):
    # The claim is a trunk commit; a run that would claim first and then
    # discover no worker can launch leaves a parked branch behind for nothing.
    monkeypatch.delenv("AGENT_CMD", raising=False)
    root = git_repo(tmp_path)
    write_spec(root, "queued", "WI-401", specref="seed.txt")
    _commit(root, "file WI-401", when=T_CODE)

    rc = drv.run(root, drive_args(agent_cmd=None), worker=None)
    assert rc == 2
    assert "no agent command wired" in capfd.readouterr().err
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert "wi-401-widget" not in _git(root, "branch", "--format=%(refname:short)")


def test_drive_unwired_config_still_drains_an_empty_queue_to_zero(
    tmp_path, capfd, monkeypatch
):
    # The config preflight is applied only when work needs a worker: an inert
    # scaffold (empty AGENT_CMD, no enable-list) with an EMPTY queue is a
    # successful drain, not a config error — the spec's empty-frontier
    # contract wins (codex cross-review, round 1).
    monkeypatch.delenv("AGENT_CMD", raising=False)
    root = git_repo(tmp_path)

    rc = drv.run(root, drive_args(agent_cmd=None), worker=None)
    assert rc == 0
    assert "queue drained" in capfd.readouterr().out


def test_a_claim_dir_with_no_branch_ref_no_longer_stops_the_run(tmp_path, capfd):
    # WI-387 DELETED `_stranded_claims`. It existed only because the claim
    # advanced trunk BEFORE cutting the branch, so a crash between the two
    # writes left a claim no lane could reach; the claim now writes the branch
    # first and that window is gone (tests/test_integrate.py drives the
    # abandoned-claim shape it leaves instead). What remains here — a
    # hand-made active/ directory with no branch — is residue, not a
    # half-claim, and residue must not stop a run that has nothing to do.
    root = git_repo(tmp_path)
    write_spec(root, "active/wi-401", "WI-401", specref="seed.txt")
    _commit(root, "residue: a hand-made claim directory", when=T_CODE)
    worker = Recorder()

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 0
    assert "queue drained" in capfd.readouterr().out
    assert worker.calls == []


def test_drive_refuses_a_dirty_trunk_before_resuming(tmp_path, capfd):
    # The claim rung's clean-trunk refusal, hoisted to the cycle top: the
    # parked-resume path must meet it too, BEFORE a worker session runs.
    root = parked_repo(tmp_path)
    (root / "scratch.txt").write_text("uncommitted\n", encoding="utf-8")
    worker = Recorder()

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 2
    assert "working tree is dirty" in capfd.readouterr().err
    assert worker.calls == []


def test_drive_empty_frontier_drains_and_exits_zero(tmp_path, capfd):
    # A finished queue is SUCCESS: the drained banner at exit 0 (the done-when
    # names this outcome explicitly — an empty frontier is not an error).
    root = git_repo(tmp_path)
    worker = Recorder()

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 0
    out = capfd.readouterr().out
    assert "queue drained" in out and "0 WI(s) integrated" in out
    assert worker.calls == []


# --- the composed refusals stop the run ---------------------------------------


def test_drive_claim_refusal_stops_the_run(tmp_path, capfd):
    # The SpecRef rung (WI-370) fires inside integrate.claim; the driver must
    # surface it and STOP — never skip to the next WI, never talk past it.
    root = git_repo(tmp_path)
    write_spec(root, "queued", "WI-401", specref=None)
    _commit(root, "file WI-401", when=T_CODE)
    worker = Recorder()

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 1
    assert "carries no SpecRef" in capfd.readouterr().err
    assert worker.calls == []
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()


def test_drive_pause_appearing_mid_run_stops_the_next_cycle(tmp_path, capfd):
    # §5.6: pause = stop claiming. The check sits at the top of EVERY cycle,
    # so a pause dropped while a worker ran stops the next claim — with the
    # pause banner (exit 8), not a claim-rung refusal.
    root = parked_repo(tmp_path)

    def drop_pause(r, branch, wi_ids):
        (r / "docs" / "work" / "pause").write_text(
            'reason = "owner says stop"\nsince = "2026-07-31"\n',
            encoding="utf-8",
            newline="\n",
        )
        _commit(r, "pause: owner says stop", when=T_LATER)

    worker = Recorder(outcomes=(0,), effect=drop_pause)
    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 8
    err = capfd.readouterr().err
    assert "PAUSED" in err and "owner says stop" in err
    assert len(worker.calls) == 1


def test_drive_resumes_a_parked_branch_and_stalls_on_no_progress(tmp_path, capfd):
    # A parked claim from an interrupted run is picked up FIRST (resume, not
    # refuse) — and a worker that keeps reporting DONE without finishing its
    # branch cannot loop forever: the trunk never moves, so the drive loop's
    # own stall guard aborts (exit 4).
    root = parked_repo(tmp_path)
    worker = Recorder(outcomes=(0, 0))

    rc = drv.run(root, drive_args(stall_limit=2), worker=worker)
    assert rc == 4
    assert "STALL" in capfd.readouterr().err
    assert worker.calls == [("wi-401", ("WI-401",)), ("wi-401", ("WI-401",))]


def test_a_crashed_worker_stays_parked_and_the_next_cycle_resumes_it(tmp_path, capfd):
    # §A3 draws the line at DECIDED vs CRASHED. A crash (an exit code the
    # worker's own vocabulary does not contain) is deliberately NOT a hang: the
    # branch exists and the specs are still in active/<branch>/, so the
    # parked-resume path handles it exactly as before and a worker that keeps
    # dying is bounded by the stall guard rather than by a run-stop.
    root = parked_repo(tmp_path)
    worker = Recorder(outcomes=(1, 1))

    rc = drv.run(root, drive_args(stall_limit=2), worker=worker)
    assert rc == 4
    err = capfd.readouterr().err
    assert "CRASHED (exit 1)" in err and "STALL" in err
    assert len(worker.calls) == 2
    assert (root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md").is_file()
    assert "wi-401" in _git(root, "branch", "--format=%(refname:short)")


# --- the third terminal outcome: HANDBACK (WI-387, §A3) -----------------------
#
# These run the WHOLE cycle — claim, worker, close, refresh, merge, next cycle —
# against a stub harness rather than a bootstrapped scaffold, because what is
# under test is the loop's decision and the shape it lands in trunk, not the
# bar. The stub check is CONDITIONAL (red exactly while the lane's own broken
# file is present), which is what lets the red-handback ruling be driven end to
# end instead of asserted about: an always-red stub could not show the second
# refresh going green. Helper shapes are copied from tests/test_integrate.py per
# this suite's no-cross-test-import idiom.

STUB_TRUNK_STEP = "pass\n"

STUB_CHECK = """import pathlib
import sys

if pathlib.Path("broken.py").exists():
    print("  FAIL  tests+coverage   exit 1 (0.2s)")
    sys.exit(1)
print("  PASS  tests+coverage   0.2s")
"""


def stub_harness_repo(tmp_path):
    """A trunk with WI-401 queued, a DECLARED bar, and a stub harness in the
    tree — the smallest repo a full drive cycle can actually run in."""
    root = git_repo(tmp_path)
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    (root / "docs" / "stack.ini").parent.mkdir(parents=True, exist_ok=True)
    # [generated] declared the way the shipped template does it: the WI-388
    # intake mint commits its regeneration in the same bookkeeping commit
    # (RULING-6), so a repo that has not declared its generated artifacts
    # would flag its own intake — same reason test_integrate.declare_generated
    # gives for the claim.
    (root / "docs" / "stack.ini").write_text(
        "[product]\ntest = {py} -m pytest -q\n"
        "[generated]\nPROJECT_STATE.html = trajectory\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "docs" / "review-policy").write_text("0\n", encoding="utf-8", newline="\n")
    scripts = root / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "trunk_step.py").write_text(
        STUB_TRUNK_STEP, encoding="utf-8", newline="\n"
    )
    (scripts / "check.py").write_text(STUB_CHECK, encoding="utf-8", newline="\n")
    write_spec(root, "queued", "WI-401", specref="seed.txt")
    _commit(root, "seed: the stub harness, the declared bar and WI-401", when=T_CODE)
    return root


def building_worker(exit_code, files=()):
    """A worker that writes `files` into its lane worktree and then reports
    `exit_code` WITHOUT closing its specs — the shape of a session that got
    part-way and then could not proceed."""

    def worker(root, branch, wi_ids, args):
        wt, err = drv.integrate.lane_worktree(root, branch)
        assert err is None, err
        for name, text in files:
            (wt / name).write_text(text, encoding="utf-8", newline="\n")
        return exit_code

    return worker


def _returned(root, wid="WI-401"):
    path = root / "docs" / "work" / "queued" / "{}-widget.md".format(wid)
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def then_closing(first_worker):
    """`first_worker` for call 1, the closing shape for every later call.

    A handback's merge now MINTS the disposition row at intake (WI-388, R3),
    and the same run drives it — so a stub worker that fails every call would
    stop the run at the R3 no-recursion refusal (the invariant working, but
    not these tests' subject). The second session records its judgement by
    drafting a successor and closing the disposition row, the way a real
    adjudication session ends — OI-73 REFUSES a partial/cancelled disposition
    that queues no successor, so the stub drafts one to stay conformant."""
    calls = []
    successor = """
## Dispositions

```toml
title = "Continue the {wi} work by another route"
workstream = "process"
buildtier = "quick"
```

Re-land the reviewed parts.
"""

    def worker(root, branch, wi_ids, args):
        calls.append((branch, tuple(wi_ids)))
        if len(calls) == 1:
            return first_worker(root, branch, wi_ids, args)
        wt, err = drv.integrate.lane_worktree(root, branch)
        assert err is None, err
        for spec in sorted((wt / "docs" / "work" / "active" / branch).glob("WI-*.md")):
            text = spec.read_text(encoding="utf-8")
            # A `disposition`-brief adjudication row must queue a successor
            # (OI-73). Draft one unless the row already carries a Dispositions
            # section (a fresh mint never does).
            if 'brief = "disposition"' in text and "\n## Dispositions\n" not in text:
                text += successor.format(wi=wi_ids[0])
            dst = wt / "docs" / "work" / "complete" / spec.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(text, encoding="utf-8", newline="\n")
            _git(wt, "rm", "-q", "docs/work/active/{}/{}".format(branch, spec.name))
        _commit(wt, "{}: adjudicated + closed".format(";".join(wi_ids)), when=T_LATER)
        return 0

    worker.calls = calls
    return worker


def test_a_needs_human_worker_hands_back_and_the_run_keeps_going(tmp_path, capfd):
    # THE RUN-STOP THIS DELETES. Exit 7 used to end the whole walk-away run
    # with the branch parked. Now the lane closes into trunk and the driver
    # carries on to the drained banner — asserted at exit 0, not just by the
    # absence of a 7, because "kept working" is the property that matters.
    root = stub_harness_repo(tmp_path)
    worker = then_closing(building_worker(7, [("half-done.py", "VALUE = 1\n")]))

    rc = drv.run(root, drive_args(), worker=worker, tier="smoke")
    assert rc == 0
    out = capfd.readouterr().out
    assert "handback: closed WI-401 as partial from wi-401-widget" in out, out
    assert "merged (WI-401=partial)" in out, out
    assert "queue drained" in out, out

    # The WI is back in trunk, blocked, with its note — and the branch is gone.
    spec = _returned(root)
    # SR-144: the spec's DEFINITION is untouched — the close's record is a
    # separate immutable report, and the folder (terminal `partial/`) is
    # what keeps the row off the frontier, so no blockref is written.
    assert "## Handback" not in spec
    assert "blockref" not in spec
    report = (root / "docs" / "handbacks" / "WI-401-wi-401-widget.md").read_text(
        encoding="utf-8"
    )
    assert 'claimed_outcome = "partial"' in report
    assert "worker exit 7 (NEEDS-JUDGEMENT)" in report
    # The dispatcher cannot judge the keep/discard split and SAYS so,
    # rather than leaving the report silent about it.
    assert 'split_decided_by = "adjudicator"' in report
    assert "wi-401-widget" not in _git(root, "branch", "--format=%(refname:short)")
    # The partial work landed in trunk, which is the whole point of handing
    # back rather than parking: a future WI can pick it up from here.
    assert (root / "half-done.py").read_text(encoding="utf-8") == "VALUE = 1\n"
    # ...and the handback's merge MINTED the disposition row at intake
    # (WI-388, ruling R3), which this same run then drove to a close.
    assert worker.calls[1][1] == ("WI-402",), worker.calls
    assert list((root / "docs" / "work" / "complete").glob("WI-402-*.md"))


def test_a_decided_exit_after_the_lane_closed_merges_on_its_declared_outcome(
    tmp_path, capfd
):
    # THE OTHER DIAGONAL of the invariant's boundary. A review escalation lands
    # at the END of a lane, so the close may already be written when the worker
    # reports a decided failure — and `hand_back` reads the claimed spec out of
    # `active/<branch>/` in the LANE, where a closed lane no longer has one. It
    # failed with an OSError and stopped the run over a branch that would have
    # merged cleanly (REVIEW-A round 1, driven). The tree has already named an
    # outcome; the drain merges it on that.
    root = stub_harness_repo(tmp_path)

    def worker(root_, branch, wi_ids, args):
        wt, err = drv.integrate.lane_worktree(root_, branch)
        assert err is None, err
        (wt / "shipped.py").write_text("VALUE = 1\n", encoding="utf-8", newline="\n")
        src = wt / "docs" / "work" / "active" / branch / "WI-401-widget.md"
        dst = wt / "docs" / "work" / "complete" / "WI-401-widget.md"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(
            src.read_text(encoding="utf-8").replace('specref = "seed.txt"\n', ""),
            encoding="utf-8",
            newline="\n",
        )
        _git(wt, "rm", "-q", "docs/work/active/{}/WI-401-widget.md".format(branch))
        _commit(wt, "WI-401: build + close", when=T_LATER)
        return 6  # EXIT_BUDGET, after the close was already written

    rc = drv.run(root, drive_args(), worker=worker, tier="smoke")
    assert rc == 0
    out = capfd.readouterr().out
    assert "already out of active/" in out, out
    assert "merged (WI-401=merged)" in out, out
    assert (root / "docs" / "work" / "complete" / "WI-401-widget.md").is_file()
    assert (root / "shipped.py").is_file()


def test_a_red_handback_is_reverted_to_a_bar_inert_artefact_and_merges(tmp_path, capfd):
    # THE RULED CASE (owner decision 1). The lane hands back code the bar
    # refuses, which would be the one branch that could still hang. Instead the
    # code is reverted, the failing diff lands as a `.patch`, the second
    # refresh goes green and the branch merges — so trunk ends with the record
    # and without the red.
    root = stub_harness_repo(tmp_path)
    worker = then_closing(building_worker(7, [("broken.py", "VALUE = (\n")]))

    rc = drv.run(root, drive_args(), worker=worker, tier="smoke")
    assert rc == 0
    captured = capfd.readouterr()
    assert "quarantining it" in captured.err, captured.err
    assert "handback: quarantined wi-401-widget" in captured.out, captured.out
    assert "merged (WI-401=partial)" in captured.out, captured.out

    assert not (root / "broken.py").exists()  # nothing live to red anything
    patch = root / "docs" / "work" / "handback" / "wi-401-widget.patch"
    assert patch.is_file()
    assert "VALUE = (" in patch.read_text(encoding="utf-8")
    # The close report survives the quarantine: it is BOOKKEEPING, and
    # reverting it would destroy the event identity the disposition mint
    # keys off — a terminal row nothing is owed a judgement for.
    assert (root / "docs" / "handbacks" / "WI-401-wi-401-widget.md").is_file()


# --- end to end against the REAL bar ------------------------------------------

E2E_GOOD_SRC = '''"""Demo module. Implements: SR-001"""


def add(a, b):
    """Add two numbers. Implements: SR-001, LLR-001"""
    return a + b
'''

E2E_BAD_SRC = '''"""Demo module. Implements: SR-001"""


def add(a, b):
    """Add two numbers. Implements: SR-001, LLR-001"""
    return a - b
'''


def scaffold_with_queued_wi(tmp_path, bar=None):
    """A bootstrapped, DevStg-Impl-complete scaffold with WI-401 queued — the state a
    plain launch starts from. Mirrors test_integrate.scaffolded_closed_branch
    (fixture notes there), except the WI is still QUEUED: claiming it is the
    driver's job under test."""
    skip_without_env_gates("git")
    repo = tmp_path / "repo"
    repo.mkdir()
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", repo], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    make_minimal_project(repo)
    # SN-028: one policy home — the scaffold ships docs/process.toml.
    set_process_key(repo, "policies", "review_rounds", 0)
    # WI-428: bootstrap.py copies the template's LIVE blackout window, and this
    # module launches the coordinator for real. Left alone, a weekday run
    # between 12:00 and 19:00 UTC would sleep instead of testing.
    disable_blackout(repo)
    with (repo / ".gitignore").open("a", encoding="utf-8", newline="\n") as fh:
        fh.write("out/\n")
    write_spec(repo, "queued", "WI-401", specref="docs/log.md", bar=bar)
    record_ids(repo)  # WI-401 is an ALLOCATED id; the mark must cover it
    _git(repo, "init", "-q")
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "config", "commit.gpgsign", "false")
    _commit(repo, "seed: the scaffolded project", when=T_BASE)
    return repo


def closing_worker(src_text):
    """The injected worker: does what a real worker session's committed
    evidence amounts to — one product commit + the closing move to complete/
    (SpecRef cleared per R-F) on the claimed branch, via its own worktree."""

    def worker(root, branch, wi_ids, args):
        wt = root.parent / ("wt-" + branch)
        _git(root, "worktree", "add", str(wt), branch)
        (wt / "src" / "demo.py").write_text(src_text, encoding="utf-8", newline="\n")
        spec = wt / "docs" / "work" / "active" / branch / "WI-401-widget.md"
        dst = wt / "docs" / "work" / "complete" / "WI-401-widget.md"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(
            spec.read_text(encoding="utf-8").replace('specref = "docs/log.md"\n', ""),
            encoding="utf-8",
            newline="\n",
        )
        _git(wt, "rm", "-q", "docs/work/active/{}/WI-401-widget.md".format(branch))
        _commit(wt, "WI-401: build + close", when=T_CODE)
        return 0

    return worker


def test_drive_end_to_end_claims_builds_merges_and_drains(tmp_path, capfd):
    repo = scaffold_with_queued_wi(tmp_path)

    rc = drv.run(repo, drive_args(), worker=closing_worker(E2E_GOOD_SRC), tier="smoke")
    assert rc == 0
    out = capfd.readouterr().out

    # The claim happened, the merge landed, the branch unloaded, the worker
    # worktree GC'd, and the drained banner counted the one integration.
    assert (repo / "docs" / "work" / "complete" / "WI-401-widget.md").is_file()
    # git tracks files, not directories: the emptied active/<branch>/ dir may
    # linger on disk — what must be gone is any claimed SPEC.
    assert not list((repo / "docs" / "work" / "active").rglob("WI-*.md"))
    branches = _git(repo, "branch", "--format=%(refname:short)")
    assert "wi-401-widget" not in branches
    assert not (repo.parent / "wt-wi-401-widget").exists()

    # THE SPECULATIVE HALF (WI-386): the driver refreshed the finished branch
    # BEFORE taking the slot, so the slot found it already merge-ready and never
    # had to fall back to refreshing in-slot. If `_drain`'s refresh call were
    # dropped, everything above would still pass and only this would fail —
    # which is the point of asserting it separately from "it merged".
    assert "integrate: refreshed wi-401-widget onto trunk" in out, out
    assert "is not merge-ready" not in out, out
    # ...and the merged tip is the refresh commit, carrying the bar's own
    # attestation for exactly that tree.
    merged_tip = _git(repo, "rev-list", "--parents", "-n", "1", "HEAD").split()[2]
    assert integ.refresh_attestation(repo, "wi-401-widget", merged_tip) is not None


def test_drive_stops_on_a_red_refresh_bar(tmp_path, capfd):
    # The worker's "close" breaks the product test: the REAL bar goes red at the
    # §A2 refresh — on the branch, where the lane that caused it can fix it —
    # and the driver STOPS with the branch still claimed. Nothing merged,
    # nothing skipped, and (unlike the composed-tree bar this replaced) nothing
    # parked on a candidate branch for someone to go and read.
    #
    # THE WI PINS ITS OWN `bar:` SINCE THE OI-30 D2 CEILING, and that is not
    # test-plumbing — it is this test proving the escape hatch the ruling rests
    # on. `sr_bar` now stops at DevStg-Tests, so a fully approved scaffold no
    # longer DERIVES DevStg-Impl, and the `tests+coverage` step is tagged for
    # DevStg-Impl alone: without the pin the broken product source below would
    # sail through a green bar. The `bar:` frontmatter key (WI-388) is exactly
    # the "`--gate DevStg-Impl` stays explicitly invocable" half of the
    # ruling, and it is what a lane that wants the strict plan uses.
    #
    # MEASURED CONSEQUENCE, NAMED FOR THE SITTING (log 2026-08-15m): under the
    # ceiling, a derived-gate plan never reaches DevStg-Impl, so
    # `tests+coverage` and `module-coverage` stop being selected by derivation
    # for every repo — they are in `check.ADVISORY_EXCLUDE`, so the open-window
    # advisory tier does not cover them either.
    repo = scaffold_with_queued_wi(tmp_path, bar="DevStg-Impl")

    rc = drv.run(repo, drive_args(), worker=closing_worker(E2E_BAD_SRC), tier="smoke")
    assert rc == 1
    err = capfd.readouterr().err
    assert "bar is RED on the refreshed tree" in err
    assert "wi-401-widget" in _git(repo, "branch", "--format=%(refname:short)")
    assert not (repo / "docs" / "work" / "complete" / "WI-401-widget.md").exists()
    # The lane is left exactly where the worker left it: no refresh commit, no
    # attestation, so the slot could not merge it even if something tried.
    assert integ.refresh_attestation(repo, "wi-401-widget") is None


# --- the spine barrier, end to end (WI-381, §A4/§A8) ---------------------------


def closing_all_worker(recorder=None):
    """A worker that closes EVERY claimed spec on its branch (specref cleared
    per R-F) — the batch-aware sibling of `closing_worker`, driving the
    admitted assignment exactly as one agent_loop --wi 'A;B' session would."""
    calls = recorder if recorder is not None else []

    def worker(root, branch, wi_ids, args):
        calls.append((branch, tuple(wi_ids)))
        wt, err = drv.integrate.lane_worktree(root, branch)
        assert err is None, err
        for spec in sorted((wt / "docs" / "work" / "active" / branch).glob("WI-*.md")):
            dst = wt / "docs" / "work" / "complete" / spec.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(
                spec.read_text(encoding="utf-8").replace('specref = "seed.txt"\n', ""),
                encoding="utf-8",
                newline="\n",
            )
            _git(
                wt,
                "rm",
                "-q",
                "docs/work/active/{}/{}".format(branch, spec.name),
            )
        _commit(wt, "{}: build + close".format(";".join(wi_ids)), when=T_LATER)
        return 0

    worker.calls = calls
    return worker


def test_the_spine_batch_admits_first_and_together(tmp_path, capfd):
    # §A4: spine rows sort first (rank 0) and admit TOGETHER as one batch on
    # one branch — the worker seam receives the whole batch (`agent_loop --wi
    # 'A;B'`, its one surviving caller) — and the ordinary row behind the
    # barrier waits for the window to close before it is admitted.
    root = stub_harness_repo(tmp_path)
    write_spec(
        root, "queued", "WI-501", slug="alpha", safety="spine", specref="seed.txt"
    )
    write_spec(
        root, "queued", "WI-502", slug="beta", safety="spine", specref="seed.txt"
    )
    _commit(root, "file the spine batch", when=T_LATER)
    worker = closing_all_worker()

    rc = drv.run(root, drive_args(), worker=worker, tier="smoke")
    assert rc == 0
    out = capfd.readouterr().out
    assert worker.calls == [
        ("wi-501-alpha", ("WI-501", "WI-502")),
        ("wi-401-widget", ("WI-401",)),
    ]
    assert "claiming WI-501;WI-502 on wi-501-alpha (exclusive)" in out, out
    complete = root / "docs" / "work" / "complete"
    for name in ("WI-501-alpha.md", "WI-502-beta.md", "WI-401-widget.md"):
        assert (complete / name).is_file(), name
    assert "queue drained" in out


def hand_finished_branch(root, rows=(("WI-777", "residue"),), branch="wi-777"):
    """A lane finished BETWEEN runs, by hand: trunk still shows its spec(s)
    under active/, while the branch has already moved them to complete/. That
    is what `finished_branches` calls residue at the next tick — finished,
    unmerged, and settled by whichever drain reaches it first.

    `rows` is a list because ONE branch may carry SEVERAL WIs (that is what an
    exclusive batch is), and a residue count that credits branches instead of
    WIs is only visible when a residue branch carries more than one. Trunk must
    already hold everything it is going to hold when this is called: the branch
    is cut from HEAD, and §A2 admits it only while trunk is still its
    ancestor."""
    for wid, slug in rows:
        write_spec(root, "active/" + branch, wid, slug=slug, specref="seed.txt")
    _commit(
        root,
        "claim: {} -> active/{} (by hand)".format(
            ";".join(w for w, _s in rows), branch
        ),
        when=T_CODE,
    )
    _git(root, "branch", branch)
    wt, err = drv.integrate.lane_worktree(root, branch)
    assert err is None, err
    for wid, slug in rows:
        name = "{}-{}.md".format(wid, slug)
        src = wt / "docs" / "work" / "active" / branch / name
        dst = wt / "docs" / "work" / "complete" / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(
            src.read_text(encoding="utf-8").replace('specref = "seed.txt"\n', ""),
            encoding="utf-8",
            newline="\n",
        )
        _git(wt, "rm", "-q", "docs/work/active/{}/{}".format(branch, name))
    _commit(wt, "hand-finished between runs", when=T_LATER)
    return branch


def test_residue_settled_at_barrier_open_is_counted_in_the_drained_banner(
    tmp_path, capfd
):
    # REVIEW-A finding 3, the reviewer's two-branch drive. The spine row opens
    # the barrier, and the barrier-open `_drain` settles the hand-finished
    # lane so the batch runs as the sole toucher of trunk. That merge is real
    # — the spec lands in complete/ — but the arm did not credit it, so the
    # run's own banner disowned a WI it had just integrated. `_station_exit`
    # has counted its residue this way since REVIEW-A round 1; this is the
    # same contract, on the other admission path.
    root = stub_harness_repo(tmp_path)
    # TWO spine rows, deliberately: they admit as ONE batch on ONE branch, so a
    # count that credits branches instead of WIs reports 3 where 4 integrated.
    # A single-WI batch cannot tell those two units apart (REVIEW-A finding 1).
    write_spec(
        root, "queued", "WI-501", slug="alpha", safety="spine", specref="seed.txt"
    )
    write_spec(
        root, "queued", "WI-502", slug="beta", safety="spine", specref="seed.txt"
    )
    _commit(root, "file the spine batch", when=T_LATER)
    # ...and the residue branch carries TWO as well, for the same reason on the
    # other counting path: the barrier-open credit is taken from the residue
    # branches, so a single-WI residue branch cannot tell WIs from branches.
    hand_finished_branch(root, rows=(("WI-777", "residue"), ("WI-778", "second")))
    worker = closing_all_worker()

    rc = drv.run(root, drive_args(), worker=worker, tier="smoke")
    assert rc == 0
    out = capfd.readouterr().out
    complete = root / "docs" / "work" / "complete"
    # All three really did integrate: the residue at barrier-open, the spine
    # batch it made way for, and the ordinary row behind the barrier.
    for name in (
        "WI-777-residue.md",
        "WI-778-second.md",
        "WI-501-alpha.md",
        "WI-502-beta.md",
        "WI-401-widget.md",
    ):
        assert (complete / name).is_file(), name
    assert "5 WI(s) integrated this run." in out, out
    # Every way this count has been wrong, pinned by name so no regression can
    # pass by printing a merely plausible number: 3 dropped the residue
    # entirely (the original finding), and 4 is either unit counted as
    # branches — the batch's second WI, or the residue branch's.
    for wrong in ("2 WI(s)", "3 WI(s)", "4 WI(s)"):
        assert wrong + " integrated this run." not in out, (wrong, out)


def test_attended_approval_row_drains_and_exits_zero_with_the_banner(tmp_path, capfd):
    # THE HONEST CORRECTION (§A8): before WI-381 a queued gate row sorted
    # first, the driver claimed ready[0], `_claim_refusal` rejected it and the
    # run stopped NONZERO — a failure banner over a machine that had finished
    # everything it was allowed to do. Under `attended` the dispatcher must
    # not dispatch an approval: drain, leave the cards on open-items.html,
    # exit 0 with the honest banner — and take no ordinary work past the
    # pending approval either (the §A8 premise: no work can be taken).
    root = git_repo(tmp_path)
    write_spec(
        root, "queued", "WI-600", slug="approve", safety="gate", specref="seed.txt"
    )
    write_spec(root, "queued", "WI-401", specref="seed.txt")
    (root / "docs" / "gate-policy").write_text(
        "attended\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "file the approval row", when=T_CODE)
    worker = Recorder()

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 0
    out = capfd.readouterr().out
    # WI-412 (REVIEW-A finding 1): this fixture is the reviewer's driven
    # corner — a queued gate row with ZERO pending cards. The banner must name
    # the queued row, NOT send the owner to a page that renders "None - no
    # durable owner action is pending".
    assert "1 queued attestation row(s)" in out, out
    assert "no card has projected to open-items.html yet" in out, out
    assert "approval(s) waiting in open-items.html" not in out, out
    assert worker.calls == []
    assert (root / "docs" / "work" / "queued" / "WI-600-approve.md").is_file()


def test_surface_banner_names_both_sources_and_never_sums_them(tmp_path, monkeypatch):
    # The mixed arm. `_pending_cards` and `surfaced` OVERLAP — one waiting row
    # can be both a projected card and a queued gate row — so they must never
    # be SUMMED. Review drove the cost of the first fix, which suppressed the
    # queued rows entirely whenever any card existed: one unrelated card hid
    # two real attestation rows. Both are named, separately, with the overlap
    # stated; no total is asserted that neither read supports.
    root = git_repo(tmp_path)
    monkeypatch.setattr(drv, "_pending_cards", lambda _root: ["one waiting card"])

    line = drv._surface_banner(root, ["WI-600", "WI-601"])

    assert "1 approval(s) waiting in open-items.html" in line, line
    assert "2 queued attestation row(s) on the frontier" in line, line
    assert "the two reads may name the same row" in line, line
    # never summed: 1 card + 2 rows must not be reported as 3 of anything
    assert "3" not in line, line

    # ...and with nothing queued, the cards arm is still exactly the classic
    # line the ruled amendment names.
    assert drv._surface_banner(root, []) == (
        "queue drained - 1 approval(s) waiting in open-items.html"
    )


# --- the empty-frontier ladder (§A4 amendment, ruled 2026-08-01) ---------------


def census_repo(tmp_path):
    """A drivable repo (declared bar + stub harness) whose registries name
    gaps and whose queue is EMPTY — the rung-1 state."""
    root = git_repo(tmp_path)
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "stack.ini").write_text(
        "[product]\ntest = {py} -m pytest -q\n"
        "[generated]\nPROJECT_STATE.html = trajectory\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "docs" / "review-policy").write_text("0\n", encoding="utf-8", newline="\n")
    scripts = root / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "trunk_step.py").write_text(
        STUB_TRUNK_STEP, encoding="utf-8", newline="\n"
    )
    (scripts / "check.py").write_text(STUB_CHECK, encoding="utf-8", newline="\n")
    req = root / "docs" / "requirements"
    req.mkdir(parents=True)
    (req / "system-requirements.csv").write_text(
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status,Phase,Area,SupersededBy\n"
        "SR-001,Widget,SN-001,Shall widget.,Because.,Widgets.,,1,Test,"
        "Approved,,,\n",
        encoding="utf-8",
        newline="\n",
    )
    (req / "stakeholder-needs.md").write_text(
        "# Needs\n\nSN-001: The product does a thing.\n",
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "seed the registries + the stub harness", when=T_CODE)
    return root


def test_empty_frontier_rung_one_mints_gap_rows_then_drives_them(tmp_path, capfd):
    # Rung 1, LIVE (WI-388): the census is handed to the intake mint, each gap
    # becomes a concrete gap-closure row in ONE bookkeeping commit, and the
    # run KEEPS DRIVING — the same walk-away loop claims, builds and merges
    # the rows it just minted. When the frontier empties again the census
    # still names the gaps (the stub worker fixed nothing), and the dedup
    # answers: every gap already carries a minted row, honest exit 0 — the
    # ladder cannot mint the same gap forever.
    root = census_repo(tmp_path)
    worker = closing_all_worker()

    rc = drv.run(root, drive_args(), worker=worker, tier="smoke")
    assert rc == 0
    out = capfd.readouterr().out
    assert "minted" in out and "gap-closure" in out, out
    assert "WI-388" in out
    # The minted rows were DRIVEN in this same run...
    assert worker.calls, out
    assert list((root / "docs" / "work" / "complete").glob("WI-*.md"))
    # ...the mint was a trunk bookkeeping commit, not a hand write...
    assert "mint: WI-" in _git(root, "log", "--format=%s")
    # ...and the second idle pass deduped rather than re-minting.
    assert "already carry minted rows" in out, out


def test_the_census_mint_refusal_stops_the_run_loudly(tmp_path, capfd, monkeypatch):
    # A mint that cannot complete must never be driven past: the run stops
    # with the refusal named (the merge-slot arm has the same contract).
    root = census_repo(tmp_path)
    monkeypatch.setattr(
        drv.intake, "mint_gap_rows", lambda *_a, **_k: ([], "the mint REFUSED (stub)")
    )
    rc = drv.run(root, drive_args(), worker=Recorder(), tier="smoke")
    assert rc == 1
    assert "the mint REFUSED (stub)" in capfd.readouterr().err


def test_empty_frontier_rung_two_banner_derives_from_the_shared_pending_read(
    tmp_path, capfd
):
    # Rung 2: census empty but a pending attestation exists — that is NOT
    # missing work. The banner's count comes from the SAME pending_block(root)
    # read the dashboard and open-items.html share (a Drafted spine row owing an
    # approval is one card), so agent-resume and the owner surfaces can never
    # disagree about what is blocking. (A blocked WI carrying a BlockRef used to
    # be that card; the blockref vocabulary retired at WI-553/OI-70, so the
    # surviving owner_card source is the spine arm.)
    root = git_repo(tmp_path)
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "system-requirements.csv").write_text(
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status,Phase,Area\n"
        "SR-700,Waiting,SN-001,Shall wait.,Because.,Waits.,,1,Test,Drafted,,\n",
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "file the drafted spine row", when=T_CODE)
    worker = Recorder()

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 0
    out = capfd.readouterr().out
    assert "queue drained - 1 approval(s) waiting in open-items.html" in out, out
    assert worker.calls == []


# --- the plain-launch seam (IF-015) -------------------------------------------


def test_plain_agent_loop_launch_enters_the_drive_mode(tmp_path, monkeypatch):
    # IF-015 v3: a plain launch (no role flag) DRIVES instead of refusing with
    # the map. On an empty registry that is the drained banner at exit 0 —
    # run as a real subprocess through agent_loop.py, the launcher's own path.
    root = git_repo(tmp_path)
    monkeypatch.setenv("AGENT_CMD", "stub-agent")
    proc = run_py([SCRIPTS / "agent_loop.py", "--root", str(root)], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "queue drained" in out
    assert "no role given" not in out


def test_a_review_owed_worker_stays_parked_and_the_next_cycle_resumes_it(
    tmp_path, capfd
):
    # C2 (docs/plans/2026-08-30-stall-guard-plan.md): exit 9 is NOT a decided
    # outcome — the lane parks with its committed work (no handback report,
    # spec still in active/) and the next cycle resumes it; the dispatcher's
    # own trunk-unmoved stall guard still bounds a lane that never lands its
    # round, WITHOUT closing it partial.
    root = parked_repo(tmp_path)
    worker = Recorder(outcomes=(drv.ac.EXIT_REVIEW_OWED, drv.ac.EXIT_REVIEW_OWED))

    rc = drv.run(root, drive_args(stall_limit=2), worker=worker)
    assert rc == 4
    captured = capfd.readouterr()
    assert "REVIEW OWED" in captured.out
    assert "STALL" in captured.err
    assert len(worker.calls) == 2
    assert (root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md").is_file()
    assert not (root / "docs" / "handbacks").exists()
    assert "wi-401" in _git(root, "branch", "--format=%(refname:short)")


def test_a_preflight_refusal_parks_the_lane_instead_of_committing_its_residue(
    tmp_path, capfd
):
    # 2026-09-04. `EXIT_PREFLIGHT` used to sit in `_WORKER_OUTCOMES`, so a
    # worker that could not even START was handed back: the lane's uncommitted
    # residue was committed as "the work so far, committed as-is (partial
    # close)" and every claimed row moved to the TERMINAL `partial/`. Measured
    # on a four-row spine batch whose resumed preflight refused three rows the
    # LANE ITSELF had closed — an outcome recorded for a failure the lane could
    # not have caused. A preflight refusal is evidence about the launch, not
    # about the work, so it parks exactly like a crash.
    root = parked_repo(tmp_path)
    worker = Recorder(outcomes=(2, 2))

    rc = drv.run(root, drive_args(stall_limit=2), worker=worker)
    assert rc == 4  # the stall guard bounds it, as it bounds a crash loop
    err = capfd.readouterr().err
    assert "REFUSED ITS PREFLIGHT (exit 2)" in err and "STALL" in err
    assert len(worker.calls) == 2
    # NOTHING was closed on its behalf: the claim is still in active/, no
    # `partial/` move, no close report.
    assert (root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md").is_file()
    assert not (root / "docs" / "work" / "partial").exists()
    assert not (root / "docs" / "handbacks").exists()
