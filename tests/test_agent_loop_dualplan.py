"""agent_loop --dual-plan — the coordinator dual-plan round end-to-end (WI-199).

The P6 done-condition: a fixture repo with a PlanMode=dual WI runs the FULL
round unattended through the real agent_loop entry — two planner sessions, the
real plan_coverage subprocess, one cross-critique each, the position-swapped
arbiter pair — with a fake agent CLI standing in for the model sessions, and
never enters the direct BUILD path. Heavy-integration class (subprocess
sessions), so the module rides SLOW_MODULES like the other dispatch tests.
"""

import os
import subprocess
import sys

from conftest import SCRIPTS, augment_env, run_py

AGENT_LOOP = SCRIPTS / "agent_loop.py"

GOAL = """# Goal brief - demo

- C1: the widget parses.
- C2: the widget renders.
"""

RUBRIC = """# Rubric - plan decomposition (fixture)

G1 solvable; G2 complete; B3 padding.
"""

# The fake CLI reads the prompt on argv, recognizes which hat it is by the
# prompt's own text, and answers with a canned, contract-honoring artifact.
# The arbiter answer is CONTENT-keyed (selects the label whose plan carries
# ALPHA), so both position-swapped runs select the same underlying plan.
FAKE_CLI = r"""
import sys

prompt = " ".join(sys.argv[1:])
if "You are the arbiter" in prompt:
    a = prompt.split("### Plan A", 1)[1].split("### Plan B", 1)[0]
    label = "A" if "ALPHA" in a else "B"
    print("PER-ANCHOR:\n- [G1] even: fixture\nVERDICT: SELECT {} ports=0\nRESIDUAL GAPS: none".format(label))
elif "You are a plan critic" in prompt:
    print("VERDICT: APPROVE findings=0")
elif "You are an independent planner" in prompt:
    # Two rival plans (ALPHA first, BETA second); which hat this call is comes
    # from a counter file next to this script - the launcher runs us twice.
    import pathlib
    marker = pathlib.Path(__file__).with_suffix(".count")
    n = int(marker.read_text()) if marker.exists() else 0
    marker.write_text(str(n + 1))
    name = "ALPHA" if n == 0 else "BETA"
    print("| Plan-WI | Title | Covers | Interfaces | Predecessors |")
    print("|---|---|---|---|---|")
    print("| P1 | {} parse unit | C1 | intra-module | |".format(name))
    print("| P2 | {} render unit | C2 | intra-module | P1 |".format(name))
    print("")
    print("## Notes")
    print("- no exclusions ({}).".format(name))
else:
    print("UNRECOGNIZED HAT")
    sys.exit(1)
"""


def make_fixture(tmp_path, plan_mode="dual"):
    root = tmp_path
    (root / "docs" / "requirements").mkdir(parents=True)
    (root / "docs" / "rubrics").mkdir(parents=True)
    (root / "docs" / "specs").mkdir(parents=True)
    (root / "out").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "specs" / "WI-002.md").write_text(GOAL, encoding="utf-8")
    (root / "docs" / "rubrics" / "plan-decomposition.md").write_text(
        RUBRIC, encoding="utf-8"
    )
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        "SR-ID,Title,Requirement\nSR-001,Widget,The widget shall widget.\n",
        encoding="utf-8",
    )
    (root / "docs" / "requirements" / "interfaces.csv").write_text(
        "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,"
        "Stability,Status,Component,Notes\n",
        encoding="utf-8",
    )
    (root / "docs" / "requirements" / "work-items.csv").write_text(
        "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,SpecRef,"
        "BuildTier,PlanMode\n"
        "WI-001,Done thing,core,,,done,shipped,docs/specs/WI-002.md,quick,\n"
        "WI-002,Widget effort (dual-plan),core,,,queued,,docs/specs/WI-002.md,"
        "strong,{}\n".format(plan_mode),
        encoding="utf-8",
    )
    (root / "docs" / "log.md").write_text("# Log\n", encoding="utf-8")
    (root / "docs" / "status.md").write_text(
        "# Status\n\n- next: WI-002\n", encoding="utf-8"
    )
    # The dispatcher journal writes out/ at the repo root; keeping it ignored
    # keeps the primary worktree clean so publication is never deferred.
    (root / ".gitignore").write_text("out/\n", encoding="utf-8")
    fake = root / "fake_agent.py"
    fake.write_text(FAKE_CLI, encoding="utf-8")
    # git init: agent_loop's preflight/lock path expects a repo-ish tree; the
    # dual-plan entry itself never commits, but run_session cwd = root.
    subprocess.run(
        ["git", "init", "-q"], cwd=str(root), check=True, capture_output=True
    )
    git_id = [
        "git",
        "-c",
        "user.email=kit-test@example.invalid",
        "-c",
        "user.name=kit-test",
    ]
    subprocess.run(
        git_id[:1] + ["add", "-A"], cwd=str(root), check=True, capture_output=True
    )
    subprocess.run(
        git_id + ["commit", "-q", "-m", "fixture"],
        cwd=str(root),
        check=True,
        capture_output=True,
    )
    return root, fake


def run_dualplan(root, fake, wi="WI-002", extra=()):
    cmd = '{} "{}" {{prompt}}'.format(sys.executable, fake)
    env = augment_env(dict(os.environ))
    env["AGENT_CMD"] = cmd
    return subprocess.run(
        [sys.executable, str(AGENT_LOOP), "--root", str(root), "--dual-plan", wi]
        + list(extra),
        cwd=str(root),
        capture_output=True,
        encoding="utf-8",
        stdin=subprocess.DEVNULL,
        env=env,
    )


def test_full_round_unattended_selects_and_files(tmp_path):
    root, fake = make_fixture(tmp_path)
    proc = run_dualplan(root, fake)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SELECT plan" in proc.stdout

    rounds = list((root / "docs" / "plans").iterdir())
    assert len(rounds) == 1 and rounds[0].name.startswith("DP-001-wi-002")
    names = {p.name for p in rounds[0].iterdir()}
    # Both plans, both critiques, the stage-1 coverage report, both arbiter
    # runs, the verdict, and the goal copy all land as tracked artifacts.
    assert {
        "goal.md",
        "plan-A.md",
        "plan-B.md",
        "coverage-coverage1.md",
        "critique-of-A.md",
        "critique-of-B.md",
        "verdict-run1.md",
        "verdict-run2.md",
        "verdict.md",
    } <= names
    verdict = (rounds[0] / "verdict.md").read_text(encoding="utf-8")
    assert "both position-swapped runs agree" in verdict

    # The selected plan's rows are filed as queued WIs hanging off WI-002.
    wi_csv = (root / "docs" / "requirements" / "work-items.csv").read_text(
        encoding="utf-8"
    )
    assert "WI-003" in wi_csv and "WI-004" in wi_csv
    assert "WI-002" in wi_csv.split("WI-003", 1)[1]  # parent edge on the row
    log = (root / "docs" / "log.md").read_text(encoding="utf-8")
    assert "dual-plan round DP-001" in log

    # And the round passes the real registry validator.
    ct = run_py([SCRIPTS / "check_trajectory.py"], cwd=root)
    assert ct.returncode == 0, ct.stdout + ct.stderr


def test_worker_path_refuses_a_dual_wi(tmp_path):
    root, fake = make_fixture(tmp_path)
    # The worker branch-guard runs first; satisfy it so the refusal under test
    # (the PlanMode=dual fail-closed check) is the one that fires.
    subprocess.run(
        ["git", "checkout", "-q", "-b", "llm/train/t1"],
        cwd=str(root),
        check=True,
        capture_output=True,
    )
    env = augment_env(dict(os.environ))
    env["AGENT_CMD"] = '{} "{}" {{prompt}}'.format(sys.executable, fake)
    proc = subprocess.run(
        [
            sys.executable,
            str(AGENT_LOOP),
            "--root",
            str(root),
            "--wi",
            "WI-002",
            "--train",
            "t1",
            "--max-iterations",
            "1",
        ],
        cwd=str(root),
        capture_output=True,
        encoding="utf-8",
        stdin=subprocess.DEVNULL,
        env=env,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "never a direct BUILD" in proc.stderr
    assert "--dual-plan WI-002" in proc.stderr


def test_flag_on_a_non_dual_wi_is_refused(tmp_path):
    root, fake = make_fixture(tmp_path, plan_mode="")
    proc = run_dualplan(root, fake)
    assert proc.returncode == 2
    assert "does not declare PlanMode=dual" in proc.stderr


def test_arbiter_disagreement_pages(tmp_path):
    root, fake = make_fixture(tmp_path)
    # A label-keyed (position-biased) fake arbiter always answers SELECT A, so
    # the swapped runs pick different underlying plans -> position-unstable.
    fake.write_text(
        FAKE_CLI.replace(
            'label = "A" if "ALPHA" in a else "B"',
            'label = "A"',
        ),
        encoding="utf-8",
    )
    proc = run_dualplan(root, fake)
    assert proc.returncode == 7, proc.stdout + proc.stderr
    assert "position-unstable" in proc.stderr
    # attended (default gate-policy) writes the NEEDS-HUMAN stop.
    assert (
        (root / "docs" / "run-state")
        .read_text(encoding="utf-8")
        .startswith("NEEDS-HUMAN")
    )


def test_missing_rubric_pages_honestly(tmp_path):
    root, fake = make_fixture(tmp_path)
    (root / "docs" / "rubrics" / "plan-decomposition.md").unlink()
    proc = run_dualplan(root, fake)
    assert proc.returncode == 7
    assert "no plan rubric on file" in proc.stderr


# --- WI-209: frontier auto-dispatch under --jobs + the serial quiet-park page --


def _dispatch_fixture(tmp_path, fake_body=FAKE_CLI):
    """The dual fixture with the repo in a subdir and the fake agent OUTSIDE
    it, so the planner hat-counter marker the fake writes next to itself never
    dirties the primary worktree (a dirty checkout defers publication)."""
    root, _fake_inside = make_fixture(tmp_path / "repo")
    fake = tmp_path / "fake_dispatch.py"
    fake.write_text(fake_body, encoding="utf-8")
    return root, fake


def _run_jobs(root, fake, gate_policy=None):
    if gate_policy:
        (root / "docs" / "gate-policy").write_text(gate_policy + "\n", encoding="utf-8")
    env = augment_env(dict(os.environ))
    env.pop("AGENT_CMD", None)
    return subprocess.run(
        [
            sys.executable,
            str(AGENT_LOOP),
            "--root",
            str(root),
            "--jobs",
            "1",
            "--agent-cmd",
            '{} "{}" {{prompt}}'.format(sys.executable, fake),
            "--poll-seconds",
            "0.2",
            "--model",
            "test",
        ],
        cwd=str(root),
        capture_output=True,
        encoding="utf-8",
        stdin=subprocess.DEVNULL,
        env=env,
    )


def _events(root):
    p = root / "out" / "dispatch" / "events.jsonl"
    if not p.exists():
        return []
    import json

    return [
        json.loads(ln)
        for ln in p.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]


def _reservations(root):
    out = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "for-each-ref",
            "--format=%(refname)",
            "refs/llm/reservations",
        ],
        capture_output=True,
        encoding="utf-8",
    ).stdout
    return {ln.rsplit("/", 1)[1] for ln in out.splitlines() if ln.strip()}


def test_dispatcher_auto_runs_a_dual_row_from_the_frontier(tmp_path):
    # The SR-066 auto-dispatch AC: a PlanMode=dual frontier row under --jobs
    # runs the round in the dispatcher (never a BUILD worker), files the
    # children on the integrated registry, closes the parent done, and
    # releases the reservation.
    root, fake = _dispatch_fixture(tmp_path)
    proc = _run_jobs(root, fake)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    reg = (root / "docs" / "requirements" / "work-items.csv").read_text(
        encoding="utf-8"
    )
    assert "WI-003" in reg and "WI-004" in reg  # children filed + published
    wi2 = [ln for ln in reg.splitlines() if ln.startswith("WI-002,")][0]
    assert ",done," in wi2 and "dual-plan round (train " in wi2
    rounds = list((root / "docs" / "plans").iterdir())
    assert len(rounds) == 1 and (rounds[0] / "verdict.md").exists()

    events = _events(root)
    assert not [e for e in events if e["event"] == "worker-start"]
    assert [e for e in events if e["event"] == "dual-plan-selected"]
    assert _reservations(root) == set()
    # The filed children remain queued (their own audit classifies them), so
    # the wave ends with queued work left: RUNNING, never a false DONE.
    assert (
        (root / "docs" / "run-state").read_text(encoding="utf-8").startswith("RUNNING")
    )


def test_dispatcher_dual_page_attended_parks_needs_human(tmp_path):
    # A position-biased arbiter PAGEs; attended gate-policy stops for the
    # human with the run-state ask naming the WI (reservation kept).
    root, fake = _dispatch_fixture(
        tmp_path,
        FAKE_CLI.replace('label = "A" if "ALPHA" in a else "B"', 'label = "A"'),
    )
    proc = _run_jobs(root, fake)  # absent gate-policy = attended
    assert proc.returncode == 7, proc.stdout + proc.stderr
    state = (root / "docs" / "run-state").read_text(encoding="utf-8")
    assert state.startswith("NEEDS-HUMAN")
    assert "WI-002" in state and "dual-plan" in state
    assert _reservations(root) == {"WI-002"}


def test_dispatcher_dual_page_autonomous_continues_pause_free(tmp_path):
    # The same PAGE under gate-policy autonomous never parks the run on a
    # human: the round is journaled + quarantined for the run and the
    # dispatcher reaches its end state (the pause-free invariant).
    root, fake = _dispatch_fixture(
        tmp_path,
        FAKE_CLI.replace('label = "A" if "ALPHA" in a else "B"', 'label = "A"'),
    )
    proc = _run_jobs(root, fake, gate_policy="autonomous")
    assert proc.returncode == 4, proc.stdout + proc.stderr  # EXIT_STALL: attention
    state = (root / "docs" / "run-state").read_text(encoding="utf-8")
    assert state.startswith("RUNNING"), state
    assert _reservations(root) == set()
    actions = [e for e in _events(root) if e["event"] == "dual-plan-page-action"]
    assert actions and actions[0]["action"] == "design-check-session"


# (The serial-driver quiet-park auto-page and its dual_only_frontier_ask
# guard were the WI-209 legacy-path half; WI-210 retired the serial resume
# driver outright, so the dispatcher's auto-dispatch above is the ONE path
# and the no-silent-park duty needs no second cover.)
