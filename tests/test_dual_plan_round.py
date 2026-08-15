"""agent_loop --dual-plan — the coordinator dual-plan round end-to-end (WI-199).

The P6 done-condition: a fixture repo with a PlanMode=dual WI runs the FULL
round unattended through the real agent_loop entry — two planner sessions, the
real plan_coverage subprocess, one cross-critique each, the position-swapped
arbiter pair — with a fake agent CLI standing in for the model sessions, and
never enters the direct BUILD path. Heavy-integration class (subprocess
sessions), so the module rides SLOW_MODULES like the other end-to-end tests.

Relocated at concurrency-restructure Phase 5 from test_agent_loop_dualplan.py:
the `--dual-plan` flag path is native agent_loop/plan_runner code and survives
the dispatcher deletion; the dispatcher's frontier auto-dispatch tests died
with it. The fixture registry is the spec-folder home (docs/work/), the only
registry format after Phase 5.
"""

import os
import subprocess
import sys

from conftest import set_process_key, SCRIPTS, augment_env, run_py, load_script

TRACE = load_script("trace")

AGENT_LOOP = SCRIPTS / "agent_loop.py"

GOAL = """# Goal brief - demo

- C1: the widget parses.
- C2: the widget renders.
"""

RUBRIC = """# Rubric - plan decomposition (fixture)

DevBar-Reqs solvable; DevBar-Tests complete; B3 padding.
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
    print("PER-ANCHOR:\n- [DevBar-Reqs] even: fixture\nVERDICT: SELECT {} ports=0\nRESIDUAL GAPS: none".format(label))
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

WI_001_SPEC = """+++
id = "WI-001"
title = "Done thing"
workstream = "core"
buildtier = "quick"
specref = "docs/specs/WI-002.md"
+++

## Deliverable

shipped
"""

WI_002_SPEC = """+++
id = "WI-002"
title = "Widget effort (dual-plan)"
workstream = "core"
buildtier = "strong"
specref = "docs/specs/WI-002.md"
planmode = "{plan_mode}"
+++
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
        "IF-ID,Direction,ThisProject,Counterpart,Contract,Req-Refs,Version,"
        "Stability,Status,Component,Notes\n",
        encoding="utf-8",
    )
    # The spec-folder registry home (the only home after Phase 5): one done
    # item in complete/, the dual-plan target queued.
    for sub in ("draft", "queued", "active", "deferred", "cancelled", "complete"):
        (root / "docs" / "work" / sub).mkdir(parents=True)
    (root / "docs" / "work" / "complete" / "WI-001-done-thing.md").write_text(
        WI_001_SPEC, encoding="utf-8"
    )
    (root / "docs" / "work" / "queued" / "WI-002-widget-effort.md").write_text(
        WI_002_SPEC.format(plan_mode=plan_mode), encoding="utf-8"
    )
    # The id watermark every scaffold ships: the round's DP and WI mints count
    # from the MARK, not from max(live), and `read_watermark`
    # REFUSES an absent file rather than reading it as "no id is taken" — so a
    # fixture without one exercises the refusal, not the round.
    (root / TRACE.WATERMARK).write_text(
        TRACE.render_watermark({s: 0 for s in TRACE.WATERMARK_SPACES}),
        encoding="utf-8",
    )
    (root / "docs" / "log.md").write_text("# Log\n", encoding="utf-8")
    (root / "docs" / "status.md").write_text(
        "# Status\n\n- next: WI-002\n", encoding="utf-8"
    )
    (root / ".gitignore").write_text("out/\n.venv/\n", encoding="utf-8")
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


def _queued_specs(root):
    return sorted(p.name for p in (root / "docs" / "work" / "queued").iterdir())


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

    # The selected plan's rows are filed as queued spec files hanging off
    # WI-002 (the folder home is the registry).
    queued = _queued_specs(root)
    child_3 = [n for n in queued if n.startswith("WI-003-")]
    child_4 = [n for n in queued if n.startswith("WI-004-")]
    assert child_3 and child_4, queued
    spec_3 = (root / "docs" / "work" / "queued" / child_3[0]).read_text(
        encoding="utf-8"
    )
    assert '"WI-002"' in spec_3  # parent edge in the child's needs
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


def test_arbiter_disagreement_on_a_loop_held_tier_stalls_not_pages(tmp_path):
    # The same position-unstable PAGE on a LOOP-HELD tier must NOT hard-gate
    # a human: the single-shot flag reaches the pause-free end state —
    # EXIT_STALL (attention), never NEEDS-HUMAN.
    root, fake = make_fixture(tmp_path)
    # SN-029: the loop-held tier — the ordinal's 0 end, where a recorded
    # verdict carries ratification authority. Declared as the LEVEL, not as
    # the retired enum word.
    set_process_key(root, "attestation", "human_ratification_through", 0)

    fake.write_text(
        FAKE_CLI.replace('label = "A" if "ALPHA" in a else "B"', 'label = "A"'),
        encoding="utf-8",
    )
    proc = run_dualplan(root, fake)
    assert proc.returncode == 4, proc.stdout + proc.stderr  # EXIT_STALL: attention
    assert "position-unstable" in proc.stderr
    assert "design-check-session" in proc.stderr  # the loop-held page action


def test_arbiter_disagreement_with_keep_nondependent_stalls_not_pages(tmp_path):
    # single-ratify rides the SAME pause-free else-arm as autonomous (both are
    # non-stop-needs-human page actions), so the flag path must reach
    # EXIT_STALL, never NEEDS-HUMAN. Braces SR-108's "autonomous/
    # single-ratify" clause at the --dual-plan entry (113-REVIEW-A follow-up).
    root, fake = make_fixture(tmp_path)
    # The retired `single-ratify` level was two facts: a human-held tier PLUS
    # `keep_nondependent`. Both are declared now, separately.
    set_process_key(root, "attestation", "human_ratification_through", 4)
    set_process_key(root, "attestation", "keep_nondependent", True)
    fake.write_text(
        FAKE_CLI.replace('label = "A" if "ALPHA" in a else "B"', 'label = "A"'),
        encoding="utf-8",
    )
    proc = run_dualplan(root, fake)
    assert proc.returncode == 4, proc.stdout + proc.stderr  # EXIT_STALL: attention
    assert "position-unstable" in proc.stderr
    assert "surface-block-continue-others" in proc.stderr  # the single-ratify action


def test_missing_rubric_pages_honestly(tmp_path):
    root, fake = make_fixture(tmp_path)
    (root / "docs" / "rubrics" / "plan-decomposition.md").unlink()
    proc = run_dualplan(root, fake)
    assert proc.returncode == 7
    assert "no plan rubric on file" in proc.stderr
