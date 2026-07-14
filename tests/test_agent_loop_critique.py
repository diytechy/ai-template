"""The subjective-quality critique loop (WI-068). Managed mode: a committing
build whose WI touches a Verification=Critique SR schedules a fresh,
provider-heterogeneous CRITIQUE session against a rubric before the next build.
Exercised end-to-end against a fake agent that plays both builder and critic, so
no test touches a real CLI. Absent an enable-list OR any Critique SR, nothing
changes (the never-breaking guarantee)."""

import csv
import subprocess
import sys

import pytest
from conftest import SCRIPTS, run_py

# The fake agent: a critic (prompt names a verdict path) writes its scripted
# verdict + commits; a builder commits `WI-050: ...` progress (so build_scope_srs
# reads WI-050 off the commit subject) and, after N builds, writes DONE.
FAKE = r"""
import argparse, os, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
with open(str(ctl / "models.txt"), "a", encoding="utf-8") as fh:
    fh.write(args.model + "\n")
with open(str(ctl / "prompts.txt"), "a", encoding="utf-8") as fh:
    fh.write("=== " + args.model + " ===\n" + args.prompt + "\n=== end ===\n")


def commit(path, msg):
    subprocess.run(["git", "add", str(path)], check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], check=True)


m = re.search(r"Write your verdict to (\S+)", args.prompt)
if m:
    vpath = pathlib.Path(m.group(1))
    vpath.parent.mkdir(parents=True, exist_ok=True)
    vpath.write_text((ctl / "verdict.txt").read_text(encoding="utf-8"), encoding="utf-8")
    commit(vpath, "critique verdict")
else:
    cf = ctl / "builds.txt"
    n = len(cf.read_text(encoding="utf-8").splitlines()) if cf.exists() else 0
    with open(str(cf), "a", encoding="utf-8") as fh:
        fh.write("b\n")
    pathlib.Path("art.txt").write_text("render " + str(n), encoding="utf-8")
    commit("art.txt", "WI-050: build the render " + str(n))
    done_after = (
        int((ctl / "done_after").read_text(encoding="utf-8"))
        if (ctl / "done_after").exists()
        else 999
    )
    if n + 1 >= done_after:
        pathlib.Path("docs/run-state").write_text("DONE", encoding="utf-8")
sys.exit(0)
"""

STATUS_MD = """# Status

## Current State

- **Open items:**
  - **Needs <human>**: OI-9 — a pending ask
"""

# SR-050 is Critique; its Requirement carries a marker so the redaction test can
# assert the intent reached the critic. TC-050 names the rubric in Parameters.
SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status\n"
)
SR_CRITIQUE = (
    'SR-050,Render realism,SN-001,"SR-INTENT-MARKER the render shall look real.",'
    '"Subjective.","Judged against the rubric.",,S,Critique,Verified\n'
)
SR_TEST = (
    'SR-050,Render realism,SN-001,"The render shall look real.",'
    '"Objective.","render(x)==y.",,S,Test,Verified\n'
)

TC_ROW = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
    "TC-050,SR-050,System,critique against the rubric,Release,"
    '"rubric=docs/rubrics/render.md; artifact=art.txt","Critic APPROVE",No,,Verified\n'
)

WI_ROW = (
    "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,SpecRef\n"
    "WI-050,Render,scripts,SR-050,,active,,docs/specs/WI-050.md\n"
)

RUBRIC = "# render rubric\n\n- G1 contact shadows are consistent\n- B1 RUBRIC-MARKER seam artifacts\n"

APPROVE = "- [MINOR] art.txt -> G1 mostly holds -> tidy -> @owner\nVERDICT: APPROVE findings=1\n"
CHANGES = (
    "- [MAJOR] art.txt -> B1 seam artifact at the join -> reseat the mesh -> @owner\n"
    "VERDICT: CHANGES-REQUESTED findings=1\n"
)


def _git(repo, *args):
    p = subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert p.returncode == 0, p.stdout + p.stderr
    return p.stdout.strip()


@pytest.fixture
def critique_repo(tmp_path):
    """A git repo wired for managed routing with a Critique SR: a medium PROVA
    builder + a strong PROVB critic (different provider). Returns (repo, control,
    cmd-template)."""
    repo = tmp_path / "repo"
    (repo / "docs" / "requirements").mkdir(parents=True)
    (repo / "docs" / "test").mkdir(parents=True)
    (repo / "docs" / "rubrics").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    (repo / "docs" / "run-phase").write_text("BUILD\n", encoding="utf-8")
    (repo / "docs" / "review-policy").write_text(
        "0\n", encoding="utf-8"
    )  # critique only
    (repo / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + SR_CRITIQUE, encoding="utf-8"
    )
    (repo / "docs" / "requirements" / "work-items.csv").write_text(
        WI_ROW, encoding="utf-8"
    )
    (repo / "docs" / "test" / "test-cases.csv").write_text(TC_ROW, encoding="utf-8")
    (repo / "docs" / "rubrics" / "render.md").write_text(RUBRIC, encoding="utf-8")

    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")

    ctl = tmp_path / "control"
    ctl.mkdir()
    (ctl / "verdict.txt").write_text(APPROVE, encoding="utf-8")
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    cmd = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    rows = [
        ["Id", "Provider", "Model", "Version", "Tier", "CmdTemplate", "Notes"],
        ["PROVA-BUILD-1", "PROVA", "builda", "1", "medium", cmd, ""],
        ["PROVB-CRIT-1", "PROVB", "critb", "1", "strong", cmd, ""],
    ]
    with open(
        str(repo / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(rows)
    (repo / "docs" / "agents-enabled").write_text(
        "PROVA-BUILD-1\nPROVB-CRIT-1\n", encoding="utf-8"
    )
    return repo, ctl, cmd


def _loop(repo, cmd, *extra):
    return run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            cmd,
            "--pause",
            "0",
            "--model",
            "default-tier",
            "--max-iterations",
            "8",
            *extra,
        ],
        cwd=repo,
    )


def _models(ctl):
    p = ctl / "models.txt"
    return p.read_text(encoding="utf-8").split() if p.exists() else []


def test_critique_scheduled_when_critique_sr_in_scope(critique_repo):
    repo, ctl, cmd = critique_repo
    (ctl / "done_after").write_text(
        "2", encoding="utf-8"
    )  # build -> critique -> build(DONE)
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # The build touching SR-050 scheduled a CRITIQUE round, logged before launch.
    assert "scheduling CRITIQUE round" in proc.stdout
    assert "SR-050" in proc.stdout
    # The critic ran on a DIFFERENT provider (heterogeneity) and wrote a verdict.
    models = _models(ctl)
    assert "builda" in models and "critb" in models
    assert list((repo / "docs" / "reviews").glob("*-CRITIQUE.md"))


def test_no_critique_when_no_critique_sr(critique_repo):
    # Same setup but SR-050 is Test, not Critique -> the layer is vacuous.
    repo, ctl, cmd = critique_repo
    (repo / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + SR_TEST, encoding="utf-8"
    )
    _git(repo, "commit", "-aqm", "make SR-050 Test")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "scheduling CRITIQUE round" not in proc.stdout
    assert "critb" not in _models(ctl)
    assert not (repo / "docs" / "reviews").exists()


def test_critique_prompt_is_redacted_and_carries_rubric_and_intent(critique_repo):
    repo, ctl, cmd = critique_repo
    (ctl / "done_after").write_text("2", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    crit_block = prompts.split("=== critb ===\n", 1)[1].split("\n=== end ===", 1)[0]
    assert "INDEPENDENT critic" in crit_block
    # The brief carried the rubric text AND the SN/SR intent...
    assert "RUBRIC-MARKER" in crit_block
    assert "SR-INTENT-MARKER" in crit_block
    # ...and NEVER the implementer's driver resume prompt / self-assessment.
    assert "resume from docs/status.md Current State" not in crit_block
    assert "assume no human is watching" not in crit_block


def test_prompt_map_slots_a_custom_critique_template(critique_repo):
    repo, ctl, cmd = critique_repo
    (ctl / "done_after").write_text("2", encoding="utf-8")
    tmpl = repo / "docs" / "prompts" / "crit.md"
    tmpl.parent.mkdir(parents=True)
    tmpl.write_text(
        "CUSTOM-CRITIQUE-MARKER — {brief}\nWrite your verdict to {verdict}\n",
        encoding="utf-8",
    )
    proc = _loop(repo, cmd, "--prompt-map", "CRITIQUE=docs/prompts/crit.md")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    assert "CUSTOM-CRITIQUE-MARKER" in prompts  # the mapped template was used
    assert "RUBRIC-MARKER" in prompts  # {brief} still slotted


def test_critique_budget_exhaustion_pages_human(critique_repo):
    # A perpetually CHANGES-REQUESTED critique trips the budget after
    # AGENT_CRITIQUE_MAX rounds and pages the human (attended -> NEEDS-HUMAN, 7).
    import os

    repo, ctl, cmd = critique_repo
    (ctl / "verdict.txt").write_text(CHANGES, encoding="utf-8")
    (ctl / "done_after").write_text("999", encoding="utf-8")  # never self-terminates
    env = dict(os.environ)
    env["AGENT_CRITIQUE_MAX"] = "2"
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "agent_loop.py"),
            "--root",
            str(repo),
            "--agent-cmd",
            cmd,
            "--pause",
            "0",
            "--model",
            "default-tier",
            "--max-iterations",
            "10",
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env=env,
    )
    assert proc.returncode == 7, proc.stdout + proc.stderr
    assert "critique budget exhausted" in proc.stdout
    state = (repo / "docs" / "run-state").read_text(encoding="utf-8").splitlines()
    assert state[0].strip() == "NEEDS-HUMAN"
    assert state[1].startswith("ask: critique budget exhausted")  # WI-127


def test_absent_enable_list_no_critique(critique_repo):
    # No agents-enabled -> managed off -> no critique scheduled (never-breaking).
    repo, ctl, cmd = critique_repo
    (repo / "docs" / "agents-enabled").unlink()
    (ctl / "done_after").write_text("1", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "scheduling CRITIQUE round" not in proc.stdout
    assert not (repo / "docs" / "reviews").exists()
